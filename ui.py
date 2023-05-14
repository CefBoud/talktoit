import logging
import time

import gradio as gr

from model import Model, get_indexable_data
from scrapy_crawler import domain_is_scrapped, start_crawler

logger = logging.getLogger(__name__)

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # Hey there, let's get started. The goal is to talk to your data, Talktoit 😃
        
        """
    )
    gr.Markdown(
        """
        ##  1️⃣ Scrape a website by simply entering its URL   
        
        """
    )
    with gr.Accordion("👉", open=False):
        gr.Markdown(
            """
        #### Build an index by scraping a domain starting at `start_url` and crawling up to ~ `max_pages` pages.
        s
        ###### The scraper can slightly exceed `max_pages` because the shutdown is graceful when the limit is reached.
        """
        )
        with gr.Box():
            domain_index = gr.Textbox(
                label="Domain", placeholder="example.com", max_lines=1
            )
            start_url = gr.Textbox(
                "",
                label="Start url",
                placeholder="https://www.example.com",
                max_lines=1,
            )
            max_pages = gr.Number(5, label="~ Max pages")

            scrap_status = gr.Textbox(label="Scrape Status")  # , visible=False)
            scrap_btn = gr.Button("Scrape!")

    gr.Markdown(
        """
        ##  2️⃣ Build your index
        
        """
    )

    with gr.Accordion("👉", open=False):
        with gr.Box():
            dir_to_index_dropdown = gr.Dropdown(
                get_indexable_data(),
                label="Data to index",
                info="Choose one of the available data directories to index",
            )
            create_index_btn = gr.Button("Create Index")

            build_text_output = gr.Textbox(label="Build Status")  # , visible=False)

    gr.Markdown(
        """
        ##  3️⃣ Talk
        
        """
    )
    with gr.Accordion("👉", open=False):
        with gr.Box():
            # domain_chat = gr.Textbox(label="Domain", placeholder="example.com",max_lines=1)
            available_indices = Model.get_available_indices()
            domain_chat_dropdown = gr.Dropdown(
                available_indices,
                label="Index",
                info="Choose one of the available indices or build a new one ☝️",
            )
            chatbot = gr.Chatbot()
            msg = gr.Textbox(label="Input")
            clear = gr.Button("Clear History")

    def user(user_message, history):
        return "", history + [[user_message, None]]

    def bot(domain, history):
        model = Model(domain)
        model.load_index()

        user_msg = history[-1][0]
        # bot_message = random.choice(["How are you?", "I love you", "I'm very hungry"])
        bot_message = model.query(user_msg)
        history[-1][1] = ""
        for character in bot_message:
            history[-1][1] += character
            time.sleep(0.05)
            yield history

    def create_index(dir_to_index_dropdown, progress=gr.Progress()):
        model = Model(dir_to_index_dropdown)
        # PROGRESS BAR NOT WORKING ?????
        print("starting progress")
        progress(0, desc="Starting...")
        time.sleep(0.5)
        progress(0.1, desc="inprogress...")
        try:
            model.construct_index(force=True)
            result = "success"
        except Exception as e:
            logger.error(e, exc_info=True)
            result = "failure"
        finally:
            progress(1, desc="Done")
            # https://github.com/gradio-app/gradio/discussions/2848
            domain_chat_dropdown.choices = Model.get_available_indices()
            return {
                build_text_output: gr.update(value=result),
                domain_chat_dropdown: gr.update(choices=Model.get_available_indices()),
            }

    def scrape(domain, start_url, max_pages, progress=gr.Progress()):
        logger.debug(
            f"scraping {domain}, starting with url  {start_url} and getting at most {max_pages} pages"
        )
        result = ""
        progress(0, desc="Starting...")
        time.sleep(0.5)
        progress(0.1, desc="inprogress...")
        try:
            start_urls = [] if not start_url else [start_url]

            start_crawler(
                domain,
                start_urls,
                int(max_pages),
                success_callback=lambda _: print("my gradio callback :))))"),
            )

            if domain_is_scrapped(domain):
                result = "success"
            else:
                raise Exception("domain folder has no files")
        except Exception as e:
            logger.error(e, exc_info=True)
            result = "failure"
        finally:
            progress(1, desc="Done")

            dir_to_index_dropdown.choices = get_indexable_data()
            return {
                scrap_status: gr.update(value=result),
                dir_to_index_dropdown: gr.update(choices=get_indexable_data()),
            }

    scrap_btn.click(
        scrape,
        [domain_index, start_url, max_pages],
        [scrap_status, dir_to_index_dropdown],
        queue=False,
    )

    create_index_btn.click(
        create_index,
        [dir_to_index_dropdown],
        [build_text_output, domain_chat_dropdown],
        show_progress=True,
    )

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, [domain_chat_dropdown, chatbot], chatbot
    )

    clear.click(lambda: None, None, chatbot, queue=False)
