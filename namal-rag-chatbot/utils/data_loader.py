import json
from langchain_core.documents import Document


def load_namal_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    documents = []

    for category, items in data.items():

        # Handle list-based sections
        if isinstance(items, list):

            for item in items:

                content = json.dumps(item, ensure_ascii=False, indent=2)

                doc = Document(
                    page_content=content,
                    metadata={
                        "source": category
                    }
                )

                documents.append(doc)

        # Handle dictionary-based sections
        elif isinstance(items, dict):

            content = json.dumps(items, ensure_ascii=False, indent=2)

            doc = Document(
                page_content=content,
                metadata={
                    "source": category
                }
            )

            documents.append(doc)

    return documents