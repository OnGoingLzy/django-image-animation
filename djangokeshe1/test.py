import json
import os
import openai

openai.api_key = "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"
# for x in range(1, 35):
#     day = x
completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user",
                "content": "我在A公司上班,我所在的业务板块要转让给B公司,但是B公司不一定会使用我,假如B公司不使用我,或者工资待遇不如A公司,我该如何维权,是否可以申请N+1赔款"}]
    )
print("回复:" + completion["choices"][0]["message"]["content"])
# print(completion)
