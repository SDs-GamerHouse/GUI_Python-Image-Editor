import PySimpleGUI as psg
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
from io import BytesIO

psg.theme("DarkBlue")

image_path = "Resume_Projects/image_editor/Default Image.png"
original_image = Image.open(image_path)

controls_col = psg.Column([
    [psg.Frame("Contrast",layout=[[psg.Slider(range=(0,10),orientation="horizontal",key="CONTRAST")]])],
    [psg.Frame("Blur",layout=[[psg.Slider(range=(0,10),orientation="horizontal",key="BLUR")]])],
    [psg.Frame("Rotate",layout=[[psg.Slider(range=(0,360),orientation="horizontal",key="ROTATE")]])],
    [psg.Frame("Vibrance",layout=[[psg.Slider(range=(1,5),orientation="horizontal",key="VIBRANCE")]])],
    [psg.Checkbox("Flip X",key="FLIPX"),psg.Checkbox("Flip Y",key="FLIPY"),psg.Checkbox("Emboss",key="EMBOSS")],
    [psg.Checkbox("Contour",key="CONTOUR"),psg.Checkbox("Black&White",key="B&W")],
    [psg.Button("Upload Image",key="UPLOAD"), psg.Button("Save Image",key="SAVE")]
    ])

image_col = psg.Column([[psg.Image(image_path,key="IMAGE")]])

layout = [[controls_col,image_col]]

window = psg.Window("Image Editor", layout)

def edit_image(original,contrast,blur,rotate,vibrance,flipx,flipy,emboss,contour,bw):
    global image
    image = original.filter(ImageFilter.UnsharpMask(contrast))
    image = image.filter(ImageFilter.GaussianBlur(blur))
    image = image.rotate(rotate,expand=True)
    image = ImageEnhance.Color(image).enhance(vibrance)
    if flipx:
        image = ImageOps.mirror(image)
    if flipy:
        image = ImageOps.flip(image)
    if emboss:
        image = image.filter(ImageFilter.EMBOSS())
    if contour:
        image = image.filter(ImageFilter.CONTOUR())
    if bw:
        image = ImageEnhance.Color(image).enhance(0)

    # Converting image so computer can read
    bio = BytesIO()
    image.save(bio, format="PNG")

    # Updating the image to show edits
    window["IMAGE"].update(data=bio.getvalue())

while True:
    event, values = window.read(timeout=50)
    if event == psg.WINDOW_CLOSED:
        break
    edit_image(original_image,values["CONTRAST"],values["BLUR"],values["ROTATE"],values["VIBRANCE"],values["FLIPX"],values["FLIPY"],values["EMBOSS"],values["CONTOUR"],values["B&W"])

    if event == "SAVE":
        save_path = psg.popup_get_file("Save",save_as=True,no_window=True) + ".png"
        image.save(save_path,"PNG")

    if event == "UPLOAD":
        image_path = psg.popup_get_file("Open",no_window=True)
        original_image = Image.open(image_path)

window.close()