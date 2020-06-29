import asyncio

from mini.apis import errors
from mini.apis.api_expression import ControlBehavior, ControlBehaviorResponse, RobotBehaviorControlType
from mini.apis.api_expression import ControlMouthLamp, ControlMouthResponse
from mini.apis.api_expression import PlayExpression, PlayExpressionResponse, RobotExpressionType
from mini.apis.api_expression import SetMouthLamp, SetMouthLampResponse, MouthLampColor, MouthLampMode
from mini.apis.base_api import MiniApiResultType
from mini.dns.dns_browser import WiFiDevice
from test.test_connect import test_connect, shutdown, test_start_run_program
from test.test_connect import test_get_device_by_name


# 测试让眼睛演示个表情
async def test_play_expression():
    """测试播放表情

    让机器人播放一个名为"codemao1"的内置表情，并等待回复结果

    #PlayExpressionResponse.isSuccess : 是否成功

    #PlayExpressionResponse.resultCode : 返回码

    """
    # express_type: INNER 是指机器人内置的不可修改的表情动画, CUSTOM 是放置在sdcard/customize/expresss目录下可被开发者修改的表情
    block: PlayExpression = PlayExpression(express_name="codemao1", express_type=RobotExpressionType.INNER)
    # response: PlayExpressionResponse
    (resultType, response) = await block.execute()

    print(f'test_play_expression result: {response}')

    assert resultType == MiniApiResultType.Success, 'test_play_expression timetout'
    assert response is not None and isinstance(response,
                                               PlayExpressionResponse), 'test_play_expression result unavailable'
    assert response.isSuccess, 'play_expression failed'


# 测试, 让机器人跳舞/停止跳舞
async def test_control_behavior():
    """测试控制表现力

    让机器人开始跳一个名为"dance_0004"的舞蹈，并等待回复结果

    """
    # control_type: START, STOP
    block: ControlBehavior = ControlBehavior(name="dance_0004", control_type=RobotBehaviorControlType.START)
    # response ControlBehaviorResponse
    (resultType, response) = await block.execute()

    print(f'test_control_behavior result: {response}')
    print(
        'resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_express_error_str(response.resultCode)))

    assert resultType == MiniApiResultType.Success, 'test_control_behavior timetout'
    assert response is not None and isinstance(response,
                                               ControlBehaviorResponse), 'test_control_behavior result unavailable'
    assert response.isSuccess, 'control_behavior failed'


# 测试, 设置嘴巴灯颜色为绿色 常亮
async def test_set_mouth_lamp():
    # mode: 嘴巴灯模式，0：普通模式，1：呼吸模式
    # color: 嘴巴灯颜色，1：红色，2：绿色，3：蓝色
    # duration: 持续时间，单位为毫秒，-1表示常亮
    # breath_duration: 闪烁一次时长，单位为毫秒

    """测试设置嘴巴灯

    设置机器人嘴巴灯正常模式、绿色、常亮3s，并等待回复结果

    当mode=NORMAL时，duration参数起作用，表示常亮多久时间

    当mode=BREATH，breath_duration参数起作用，表示多久呼吸一次

    #SetMouthLampResponse.isSuccess : 是否成功

    #SetMouthLampResponse.resultCode : 返回码

    """

    block: SetMouthLamp = SetMouthLamp(color=MouthLampColor.GREEN, mode=MouthLampMode.NORMAL,
                                       duration=3000, breath_duration=1000)
    # response:SetMouthLampResponse
    (resultType, response) = await block.execute()

    print(f'test_set_mouth_lamp result: {response}')

    assert resultType == MiniApiResultType.Success, 'test_set_mouth_lamp timetout'
    assert response is not None and isinstance(response, SetMouthLampResponse), 'test_set_mouth_lamp result unavailable'
    assert response.isSuccess or response.resultCode == 504, 'set_mouth_lamp failed'


# 测试,开关嘴巴灯
async def test_control_mouth_lamp():
    """测试控制嘴巴灯

    让机器人嘴巴灯关闭，并等待结果

    #ControlMouthResponse.isSuccess : 是否成功

    #ControlMouthResponse.resultCode : 返回码

    """
    # is_open: True,False
    # response :ControlMouthResponse
    (resultType, response) = await ControlMouthLamp(is_open=False).execute()

    print(f'test_control_mouth_lamp result: {response}')

    assert resultType == MiniApiResultType.Success, 'test_control_mouth_lamp timetout'
    assert response is not None and isinstance(response,
                                               ControlMouthResponse), 'test_control_mouth_lamp result unavailable'
    assert response.isSuccess or response.resultCode == 504, 'control_mouth_lamp failed'


if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())
        asyncio.get_event_loop().run_until_complete(test_play_expression())
        asyncio.get_event_loop().run_until_complete(test_set_mouth_lamp())
        asyncio.get_event_loop().run_until_complete(test_control_mouth_lamp())
        asyncio.get_event_loop().run_until_complete(test_control_behavior())
        asyncio.get_event_loop().run_until_complete(shutdown())
