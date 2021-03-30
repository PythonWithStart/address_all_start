from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Path
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware  # 引入 CORS中间件模块
from plot_fund_class import getData

import uvicorn

app = FastAPI()
# 设置允许访问的域名
origins = [
    "http://127.0.0.1",
    "http://127.0.0.1:9527",
    "http://127.0.0.1:5000",
    "http://localhost:9527",
    "*"
    # 也可以设置为"*"，即为所有。
]
# 设置跨域传参
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 设置允许的origins来源
    allow_credentials=True,
    allow_methods=["*"],  # 设置允许跨域的http方法，比如 get、post、put等。
    allow_headers=["*"])  # 允许跨域的headers，可以用来鉴别来源等作用。


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.get('/user/login')
def login():
    return {"code": 20000, "data": {"token": "admin"}}


@app.post('/api/user/login')
def login():
    return {"code": 20000, "data": {"token": "admin"}}


@app.post("/api/user/logout")
def logout():
    return {"code": 20000, "data": "success"}


@app.get("/api/user/info")
def userinfo(token: str):
    return {
        "code": 20000,
        "data": {
            "roles": [token],
            "introduction": "I am a super administrator",
            "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif",
            "name": f"Super {token}"
        }
    }


@app.get("/api/user/funddata")
async def user_funddata(fundCode: str):
    gda = getData()
    print("测试-------", fundCode)
    if fundCode == "":
        itemVal = {
            "code": 20000,
            "data": {
                "chartText": "基金测评-测试",
                "lendVal": ["星期三", "星期四", "星期五"],
                "xAxisData": ['13:00', '13:05', '13:10', '13:15', '13:20', '13:25', '13:30', '13:35', '13:40', '13:45',
                              '13:50',
                              '13:55'],
                "valDatas": [[220, 182, 191, 134, 150, 120, 110, 125, 145, 122, 165, 122],
                             [120, 110, 125, 145, 122, 165, 122, 220, 182, 191, 134, 150],
                             [220, 182, 125, 145, 122, 191, 134, 150, 120, 110, 165, 122]
                             ]
            }
        }
    else:
        rvals = gda.run_one(fund_code=fundCode)
        if rvals is None:
            itemVal = {
                "code": 20000,
                "data": {
                    "chartText": f"基金测评-无效数据-{fundCode}",
                    "lendVal": ["星期三", "星期四", "星期五"],
                    "xAxisData": ['00', '05', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55'],
                    "valDatas": [
                        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                        [90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90],
                        [110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110],
                    ]
                }
            }
        else:
            three_vals, vals = rvals
            itemVal = {
                "code": 20000,
                "data": {
                    "chartText": f"基金测评-{fundCode}",
                    "lendVal": ["星期三", "星期四", "星期五"],
                    "xAxisData": three_vals[0],
                    "valDatas": [
                        three_vals[1],
                        three_vals[2],
                        three_vals[3],
                    ]
                }
            }
    return JSONResponse(itemVal)


@app.get("/api/article/list")
def get_list():
    # 获取所有基金的最新更新数据
    return {"code": 20000, "data":
        {"total": 100, "items": [
            {"id": 1,
             "fund_id": 1,
             "timestamp": 1367472535979,
             "totalweek": "Eric",
             "matchweek": "<p>I am testing data, I am testing data.</p ><p>< img src=\"https://wpimg.wallstcn.com/4c69009c-0fd4-4153-b112-6cb53d1cf943\"></p >",
             "forecast": 77.08,
             "recommend": 2,
             "type": "EU",
             "status": "",
             }
        ]
         }
            }
