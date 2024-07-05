import chainlit as cl
from model import stream_gemini_response
from markdown_pdf import MarkdownPdf, Section



@cl.on_chat_start
def start_chat():
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are a helpful assistant."}],
    )


@cl.on_message
async def main(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})


    msg = cl.Message(content="",author="Tommy")
    response = ""
    async for chunk in stream_gemini_response(message.content):
        await msg.stream_token(chunk)
        response += chunk
    await msg.send()

    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()


    # pdf = MarkdownPdf()
    # pdf.add_section(Section(response, toc=False))
    # pdf.save('output2.pdf')
    # await cl.Message(content="Download pdf",elements=[cl.File(name="visa.pdf", path = "output2.pdf")],author="Tommy").send()
    