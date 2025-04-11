import aiohttp
import asyncio

async def send_to_google_form(id, id_to_hoc, result, trung=False):
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLScPSvuYFFJkqthsQN8nGmdi-hQOQU_2qQ98EkQPGb4TuG7QfA/formResponse"

    form_payload = {
        'entry.31662442': f"'{id}",
        'entry.955688115': f"'{str(id_to_hoc)}",
        'entry.963488546': 'Trùng lịch!' if trung else 'Thành công!',
        'entry.645101552': result[4:33] if trung else result[:19]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(form_url, data=form_payload) as response:
            if response.status == 200:
                print("✅ Gửi thành công!")
            else:
                print(f"❌ Lỗi khi gửi: {response.status}")

# 👉 Gọi thử
asyncio.run(send_to_google_form(12345, 6301734179561308646, "2025-04-11 12:34:56"))
