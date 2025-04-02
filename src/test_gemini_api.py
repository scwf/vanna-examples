from google import genai

client = genai.Client(api_key="xxx")

response = client.models.generate_content(
    model="gemini-2.0-flash-lite",
    contents="介绍AI的发展历程",
)

print(response.text)