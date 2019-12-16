import asyncio,time


async def foo(x):  # 异步定义,协程定义
    for i in range(3):
        print('foo {}'.format(i))
        await play()  # 不可以出现yield,使用await替换


async def play():
    print("play!!!!!1------------------------------------")
    await asyncio.sleep(1)
    print("play!!!!!2")

async def doing():
    print(123)

print(asyncio.iscoroutinefunction(foo))
loop = asyncio.get_event_loop()
a =loop.run_until_complete(asyncio.wait([play(),foo(1),doing()]))  # 传入一个协程对象的调用
loop.close()

