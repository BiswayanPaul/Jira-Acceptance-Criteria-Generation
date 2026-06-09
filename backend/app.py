from fastapi import FastAPI
from pydantic import BaseModel

from llm import generate_acceptance_criteria

app = FastAPI()


class StoryRequest(BaseModel):
    stories: list[str]


@app.post("/generate")
def generate(data: StoryRequest):

    results = []

    for story in data.stories:

        criteria = generate_acceptance_criteria(
            story
        )

        results.append(
            {
                "story": story,
                "acceptance_criteria": criteria
            }
        )

    return {
        "results": results
    }