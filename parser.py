import requests
import re

# Список каналов: Название и его ID на сайте rustv.live
channels = [
    {"name": "Россия 1", "id": "2"},
    {"name": "Вайнах ТВ", "id": "211"},
    {"name": "Россия К", "id": "4"}
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'rustv.live'
}

playlist_content = "#EXTM3U\n"

for ch in channels:
    source_url = f"rustv.livechannel/{ch['id']}"
    try:
        response = requests.get(source_url, headers=headers, timeout=10)
        # Ищем ссылку с токеном wmsAuthSign
        match = re.search(r'https://[a-z0-9\.]+/live/[^\s"\']+\.m3u8\?wmsAuthSign=[^\s"\']+', response.text)
        
        if match:
            stream_url = match.group(0)
            playlist_content += f"#EXTINF:-1,{ch['name']}\n{stream_url}\n"
            print(f"Ссылка для {ch['name']} получена.")
        else:
            print(f"Не удалось найти поток для {ch['name']}")
    except Exception as e:
        print(f"Ошибка при обработке {ch['name']}: {e}")

# Записываем всё в один файл
with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(playlist_content)
