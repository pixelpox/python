from adb.client import Client as AdbClient


def screenshot(deviceAddress = 'ce031713383080fa0c' , destFolder = 'screenshot' , imageName = "ADBScreenshot.png"):
    client = AdbClient(host="127.0.0.1", port=5037)
    device = client.device(deviceAddress)


    result = device.screencap()

    try:
        with open(destFolder +"/"+imageName , "wb") as fp:
            fp.write(result)
    except FileNotFoundError:
        print("could not file file or folder")

screenshot()