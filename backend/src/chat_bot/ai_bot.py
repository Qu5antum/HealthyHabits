import google.generativeai as genai
from backend.src.config.config import config

genai.configure(api_key=config.ai_api_key)

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash-lite",
)


async def ask_ai(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text.strip()


async def ai_response(user_prompt: str):
    health_check = await ask_ai(
        f"Bu mesaj sağlık alışkanlıklarıyla ilgili mi? Sadece 'yes' veya 'no' ile cevap ver:\n{user_prompt}"
    )

    if health_check.lower() != "yes":
        return "Bu konu sağlıklı alışkanlıklarla ilgili görünmüyor. Bu konuda yardımcı olabilirim"


    clarity_check = await ask_ai(
        f"Bu mesaj açık mı? Sadece 'clear' veya 'unclear' ile cevap ver:\n{user_prompt}"
    )

    if clarity_check.lower() != "clear":
        return "Tam olarak anlayamadım, biraz daha ayrıntı verebilir misin?"


    final_prompt = f"""
    Sen HabitCoach AI'sın.
    Sadece sağlık, alışkanlıklar örnek olarak su içme, spor yapma gibi, motivasyon hakkında cevap ver.
    Tıbbi teşhis verme.
    Kısa, arkadaşça ve net şekilde cevap ver.

    Kullanıcı mesajı:
    {user_prompt}
    """

    answer = await ask_ai(final_prompt)
    return answer
