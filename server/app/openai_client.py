import time
from openai import OpenAI
from dotenv import load_dotenv
import os
import pandas as pd
import ast
from scipy import spatial
import tiktoken

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL")
GPT_MODEL = os.environ.get("GPT_MODEL")

client = OpenAI(api_key=OPENAI_API_KEY)

embeddings_path = "winter_olympics_2022.csv"
df = pd.read_csv(embeddings_path)
df['embedding'] = df['embedding'].apply(ast.literal_eval)


class Assist:
    def __init__(self, assist_id) -> None:
        self.assist_id = assist_id

    def create_thread(self):
        return client.beta.threads.create()

    # def ask(self, thread_id, question):
    #     msg = client.beta.threads.messages.create(
    #         thread_id=thread_id,
    #         role="user",
    #         content=question,
    #     )

    #     run = client.beta.threads.runs.create(
    #         thread_id=thread_id,
    #         assistant_id=self.assist_id,
    #     )

    #     return run, msg

    # def wait_answer(self, run, thread_id):
    #     while run.status == "queued" or run.status == "in_progress":
    #         run = client.beta.threads.runs.retrieve(
    #             thread_id=thread_id,
    #             run_id=run.id,
    #         )
    #         time.sleep(0.5)
    #     return run

    # def answer(self, msg, thread_id):
    #     messages = client.beta.threads.messages.list(
    #         thread_id=thread_id, order="desc", limit=2)
    #     anss = filter(lambda m: m.role == 'assistant', messages)
    #     return self.format_answer(next(anss))

    # def format_answer(self, m):
    #     return f"{m.content[0].text.value}"


# search function
def strings_ranked_by_relatedness(query: str, df: pd.DataFrame, relatedness_fn=lambda x, y: 1 - spatial.distance.cosine(x, y), top_n: int = 100) -> tuple[list[str], list[float]]:
    query_embedding_response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=query,
    )
    query_embedding = query_embedding_response.data[0].embedding
    strings_and_relatednesses = [
        (row["text"], relatedness_fn(query_embedding, row["embedding"]))
        for i, row in df.iterrows()
    ]
    strings_and_relatednesses.sort(key=lambda x: x[1], reverse=True)
    strings, relatednesses = zip(*strings_and_relatednesses)
    return strings[:top_n], relatednesses[:top_n]


# query the system
def query_message(query: str, df: pd.DataFrame, model: str, token_budget: int) -> str:
    strings, relatednesses = strings_ranked_by_relatedness(query, df)
    introduction = 'Use the below articles on the 2022 Winter Olympics to answer the subsequent question. If the answer cannot be found in the articles, write "I could not find an answer."'
    question = f"\n\nQuestion: {query}"
    message = introduction
    for string in strings:
        next_article = f'\n\nWikipedia article section:\n"""\n{string}\n"""'
        if num_tokens(message + next_article + question, model=model) > token_budget:
            break
        else:
            message += next_article
    return message + question


def ask_using_embedding(query: str, thread_id: str):
    message = query_message(query, df, model=GPT_MODEL,
                            token_budget=4096 - 500)
    messages = [
        {"role": "system", "content": "You answer questions about the 2022 Winter Olympics."},
        {"role": "user", "content": message},
        {"role": "system", "content": thread_id}
    ]
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=messages,
        temperature=0,
    )
    response_message = response.choices[0].message.content
    return response_message


def num_tokens(text: str, model: str) -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))
