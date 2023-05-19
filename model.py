import logging
import os
import sys
from pathlib import Path

from langchain import OpenAI
from llama_index import (GPTKeywordTableIndex, LLMPredictor, ServiceContext,
                         SimpleDirectoryReader, StorageContext,
                         load_index_from_storage)

import conf

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


logger = logging.getLogger(__name__)



class Model:
    @classmethod
    def get_available_indices(cls):
        storage_path = Path(conf.INDEX_STORAGE_DIR)
        return [
            f.name
            for f in os.scandir(storage_path)
            if f.is_dir() and cls.index_exists(f)
        ]

    def __init__(self, domain, model_name="gpt-3.5-turbo") -> None:
        self.domain = domain
        self.index_storage_dir = f"{conf.INDEX_STORAGE_DIR}/{domain}"

        self.data_dir = f"{conf.DATA_DIR}/{domain}"
        Path(self.index_storage_dir).mkdir(exist_ok=True)

        self.llm_predictor = LLMPredictor(
            llm=OpenAI(temperature=0, model_name=model_name)
        )
        self.service_context = ServiceContext.from_defaults(
            llm_predictor=self.llm_predictor
        )

        # if init_index:
        #     if self.index_exists(self.index_storage_dir):
        #         self.index = self.load_index()
        #     else:
        #         self.index = self.construct_index()
        # else:
        self.index = None

    @classmethod
    def index_exists(cls, index_storage_dir):
        return (Path(index_storage_dir) / "index_store.json").exists()

    def construct_index(self, force=False) -> None:
        """
        force : recreate index even if it exists
        """

        logger.info("inside construct_index")

        if force or not self.index_exists(self.index_storage_dir):
            logger.info("Constructing index ..")
            documents = SimpleDirectoryReader(self.data_dir).load_data()
            index = GPTKeywordTableIndex.from_documents(
                documents, service_context=self.service_context
            )
            index.storage_context.persist(self.index_storage_dir)

        else:
            logger.info("index already exists")

    def load_index(self) -> None:
        storage_context = StorageContext.from_defaults(
            persist_dir=self.index_storage_dir
        )
        self.index = load_index_from_storage(storage_context)

    def query(self, query_string):
        if self.index:
            query_engine = self.index.as_query_engine(
                service_context=self.service_context
            )
            response = query_engine.query(query_string)
            print(response)
            return str(response)
        else:
            logger.info("index is not defined. Please load or construct it.")
