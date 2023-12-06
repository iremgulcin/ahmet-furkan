import openai
openai.api_key = 'your_openai_api_key'

def gpt_response(bloody_results):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {
                "role": "system",
                "content": "Doktor gibi davranmanı istiyorum. Verilen tahlillerden sadece referans aralığı dışında olan değerleri özet bir şekilde yorumlamanı istiyorum ve ne yapmam gerektiğini özet bir şekilde anlatmanı istiyorum. Türkçe olarak yanıt ver."
            },
            {
                "role": "user",
                "content": bloody_results
            }
        ]
    )
    print(response['choices'][0]['message']['content'])
    return response['choices'][0]['message']['content']



def format_output(data):
    formatted_data = []
    for test in data:
        formatted_data.append(f"İşlem Adı: {test['TestName']}, Sonuç: {test['Result']} {test['ResultUnit']}, Referans Değeri: {test['ReferenceValue']}")
    return formatted_data

def list_to_string(lst):
    return "\n".join(lst)