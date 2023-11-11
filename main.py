import dearpygui.dearpygui as dpg
import time

dpg.create_context()

class floatvar:
    def __init__(self, tag, value=0.0):
        self.tag = tag
        self.value = value
    def set(self, value):
        self.value = value
        dpg.set_value(self.tag, self.value)
    def get(self):
        return self.value

class listvar:
    def __init__(self, tag):
        self.tag = tag
        self.value = dpg.get_value(self.tag)
    def set(self, value):
        self.value = sorted(value)
        dpg.configure_item(self.tag, items=self.value)
    def get(self):
        return dpg.get_value(self.tag)

class ITEM:
    def __init__(self, ID, NAME, primary=False):
        self.ID = ID
        self.NAME = NAME
        self.primary = primary
    def __getitem__(self, key):
        return [self.ID, self.NAME][key]
    def __repr__(self):
        return f"|ITEM: {self.ID} {self.NAME}|"

class STRUCTURE(ITEM):
    def __repr__(self):
        return f"|STRUCTURE: {self.ID} {self.NAME}|"

class CRAFT:
    def __init__(self, id, row):
        self.ID =id
        self.IDstr = row[0]
        self.IImp = (row[1], row[2], row[3], row[4])
        self.SImp = (row[5], row[6], row[7], row[8])
        self.SExp = row[9]
        self.IExp = row[10]
    def __repr__(self):
        return f"|Craft: {self.ID} {self.IDstr} {self.IImp} {self.SImp} {self.SExp} {self.IExp}|"

def countplus():
    global Counter
    Counter +=1
    return Counter-1
def countzero():
    global Counter
    Counter = 0

class TreeNode:
    def __init__(self, item, structure, veight, veight_i, level=0, father=None):
        self.id = countplus()
        self.item = item
        self.structure = structure
        self.veight = veight
        self.veight_i = veight_i
        self.depend = []
        self.level = level
        self.father = father
        self.x, self.y = 0, self.level*400+30
    def append(self, item, structure, veight, veight_i, level=0):
        self.depend.append(TreeNode(item, structure, veight, veight_i, level, self.id))
    def print(self):
        global TEMPID
        if not(self.item in TEMPID):
            TEMPID.append(self.item)
        if not(self.structure in TEMPID) and self.structure!=None:
            TEMPID.append(self.structure)

class BinaryTree:
    def __init__(self, get):
        id_item = sITEMS[get]
        craft__ = CRAFTS[sCRAFTS[id_item]]
        self.level = 0
        self.b_tree = TreeNode(id_item, craft__.IDstr, craft__.SExp, craft__.SImp, self.level)
        for ix, i in enumerate(craft__.IImp):
            if i !=None:
                if not (i in sCRAFTS):
                    stru = None
                    veight = None
                    veight_i = (None, None, None, None)
                    self.b_tree.append(i, stru, veight, veight_i, self.level + 1)
                else:
                    craft_ = CRAFTS[sCRAFTS[i]]
                    stru = craft_.IDstr
                    veight = craft_.SExp
                    veight_i = craft_.SImp
                    self.b_tree.append(i, stru, veight, veight_i, self.level+1)
                    self.aappend(i, self.b_tree.depend[ix], self.level+1)
        return
    def aappend(self,id_item, tree, level):
        craft_ = CRAFTS[sCRAFTS[id_item]]
        for ix, i in enumerate(craft_.IImp):
            if i !=None:
                if not (i in sCRAFTS):
                    stru = None
                    veight_e = None
                    veight_i = (None, None, None, None)
                    tree.append(i, stru, veight_e, veight_i, level + 1)
                else:
                    craft = CRAFTS[sCRAFTS[i]]
                    stru = craft.IDstr
                    veight_e = craft.SExp
                    veight_i = craft.SImp
                    tree.append(i, stru, veight_e, veight_i, level+1)
                    self.aappend(i, tree.depend[ix], level+1)

X,Y = 700, 652

dpg.create_viewport(title="Calculator", small_icon="main.ico", large_icon="main.ico")
dpg.configure_viewport(0,x_pos=300, y_pos=200,width=X, height=Y, resizable=True)

DownloadVar = floatvar("Download")
ListComboboxVar = listvar("Combobox")
ITEMS = []
STRUCTURS = []
CRAFTS = []
sSTRUCTURS = {}
sITEMS = {}
sCRAFTS = {}
sLevel = {}
sFather = {}
sLinks = {}
NODES = []
initedPIC = []
Counter = 0

TEMPID = []

convertDictList = lambda s: [i[0] for i in s.items()]


def initCraft():
    global CRAFTS, sCRAFTS
    sCRAFTS = {}
    for i in CRAFTS:
        if i.IImp[0] != None:
            sCRAFTS[i.IExp] = i.ID

def DBget():
    global ITEMS, STRUCTURS, CRAFTS, sSTRUCTURS, sITEMS
    from openpyxl import load_workbook
    wb = load_workbook(filename='BD.xlsx')
    wsITEMS = wb["Items"]
    wsSTRUCTURES = wb["Structures"]
    wsCRAFTS = wb["Crafts"]
    for row in tuple(wsITEMS.values):
        ITEMS.append(ITEM(ID=row[0], NAME=row[1]))
    for row in tuple(wsSTRUCTURES.values):
        STRUCTURS.append(STRUCTURE(ID=row[0], NAME=row[1]))
    for irow, row in enumerate(tuple(wsCRAFTS.values)):
        CRAFTS.append(CRAFT(irow, row))
    for i in ITEMS:
        sITEMS[i[1]] = i[0]
    for i in STRUCTURS:
        sSTRUCTURS[i[1]] = i[0]
    initCraft()


def clear_data(sender, app_data, user_data):
    global DownloadVar, ITEMS, STRUCTURS, CRAFTS, sITEMS, sSTRUCTURS, sLevel, TEMPID, sFather, NODES
    clear_pic = True
    import os
    try:
        os.remove("BD.xlsx")
    except:
        pass
    try:
        if clear_pic:
            import shutil
            shutil.rmtree("pic")
            shutil.rmtree("TEMP")
    except:
        pass
    ITEMS, STRUCTURS, CRAFTS, sITEMS, sSTRUCTURS, sCRAFTS, sLevel, TEMPID, sFather, sLinks, NODES = [], [], [], {}, {}, {}, {}, [], {}, {}, []
    DownloadVar.set(0.0)

def update_data(sender, app_data, user_data):
    global DownloadVar, ITEMS, STRUCTURS, CRAFTS, sITEMS, sSTRUCTURS, ListComboboxVar
    dpg.bind_item_theme("Download", "theme_progressbar_blue")
    dpg.configure_item("DB1", enabled=False)
    dpg.configure_item("DB2", enabled=False)
    clear_data(sender, app_data, user_data)
    import Fparser as BD
    BD.parser(boolpic=True, DownloadVar=DownloadVar)
    DBget()
    initCraft()
    ListComboboxVar.set(convertDictList(sITEMS))
    dpg.configure_item("DB1", enabled=True)
    dpg.configure_item("DB2", enabled=True)
    dpg.bind_item_theme("Download", "theme_progressbar_green")

def START_CRAFT(sender, app_data, user_data):
    global TEMPID, sLevel, sFather, sLinks
    clear_node()
    TEMPID, sLevel, sFather, sLinks, NODES = [], {}, {}, {}, []
    countzero()
    def errorSTART():
        dpg.bind_item_theme("Calculate", "theme_button_red")
        time.sleep(1)
        dpg.bind_item_theme("Calculate", "theme_button_gr")

    item = ListComboboxVar.get()

    if item == "Select item: ":
        errorSTART()
        return
    id_item = sITEMS[item]
    if sCRAFTS.get(id_item) != None:
        TREE = BinaryTree(item)
        def pre_order(node):
            global sLevel, sFather
            if node.father in sFather:
                sFather[node.father].append(node.id)
            elif node.father != None:
                sFather[node.father] = [node.id]
            if node.level in sLevel:
                sLevel[node.level] +=1
            else:
                sLevel[node.level] = 1
            node.x = (sLevel[node.level]-1)*300+30
            node.print()
            for i in node.depend:
                pre_order(i)
        pre_order(TREE.b_tree)
        pre_init_pic()
        def order(node):
            global sLevel, sFather
            create_node(node.id, node.x, node.y, node.item, node.structure, node.veight, node.veight_i)
            for i in node.depend:
                order(i)
        order(TREE.b_tree)
        create_links()
    else:
        errorSTART()
        return

def clear_node():
    for i in NODES:
        dpg.delete_item(i)

def create_links():
    for i in list(sFather.keys()):
        for jx, j in enumerate(sFather[i]) :
            dpg.add_node_link(sLinks[i][jx+1], sLinks[j][0], parent="node_editor")

def create_node(id, x, y, item, structure, veight, veight_i):
    def _create(name, id, y, x):
        NODES.append(f"node_{id}_{name}")
        try:
            with dpg.add_node(label=f"{name}", parent="node_editor", tag=f"node_{id}_{name}", pos=[x, y]):
                pass
        except:
            pass
        dpg.bind_item_font(f"node_{id}_{name}", font01)
    def _attrib(name, id, item, veight, veight_i, type_):
        if type_==1:
            with dpg.node_attribute(parent=f"node_{id}_{name}", tag=f"node {id} out 0"):
                with dpg.drawlist(width=100, height=100):
                    dpg.draw_rectangle((0, 0), (100, 100), color=(100, 100, 100, 250), thickness=2)
                    dpg.draw_image(f"texture_{item}", [0, 0], [100, 100])
            sLinks[id] = [f"node {id} out 0"]
        else:
            with dpg.node_attribute(parent=f"node_{id}_{name}", tag=f"node {id} item-struct 2"):
                dpg.bind_item_font(dpg.add_text(f"output: {veight}"), font0)
        if type_ == 1:
            with dpg.node_attribute(parent=f"node_{id}_{name}", attribute_type=dpg.mvNode_Attr_Output, tag=f"node {id} item-struct 1"):
                dpg.bind_item_font(dpg.add_text(veight),font0)
        else:
            with dpg.node_attribute(parent=f"node_{id}_{name}", attribute_type=dpg.mvNode_Attr_Static):
                with dpg.drawlist(width=100, height=100):
                    dpg.draw_rectangle((0, 0), (100, 100), color=(100, 100, 100, 250), thickness=2)
                    dpg.draw_image(f"texture_{item}", [0, 0], [100, 100])
            for ix, i in enumerate(veight_i):
                if i!=None:
                    with dpg.node_attribute(parent=f"node_{id}_{name}", attribute_type=dpg.mvNode_Attr_Output, tag=f"node {id} inp {ix}"):
                        dpg.bind_item_font(dpg.add_text(f"input: {i}"), font0)
                    sLinks[id].append(f"node {id} inp {ix}")

    item_name = ITEMS[item - 1].NAME
    _create(item_name, id, x, y)
    _attrib(item_name, id, item, " ",None,1)
    if structure!=None:
        struct_name = STRUCTURS[structure - STRUCTURS[0].ID].NAME
        _create(struct_name, id, x, y + 200)
        _attrib(struct_name, id, structure, veight, veight_i, 2)
        dpg.add_node_link(f"node {id} item-struct 1", f"node {id} item-struct 2", parent="node_editor")

def pre_init_pic():
    from PIL import Image, ImageDraw
    from os import mkdir
    global initedPIC
    try:
        import shutil
        shutil.rmtree("TEMP")
    except:
        pass
    try:
        mkdir("TEMP")
    except:
        pass
    for i in initedPIC:
        dpg.delete_item(i)
    initedPIC = []
    for name in TEMPID:
        im1 = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
        im2 = Image.open(f"pic/{name}.png").convert('RGBA').resize((210, 210))
        im1.paste(im2, (23, 23))
        draw = ImageDraw.Draw(im1)
        draw.ellipse((0, 0, 255, 255), outline=(255, 255, 255), width=7)
        im1.save(f"TEMP/{name}.png")
        width, height, channels, data = dpg.load_image(f"TEMP/{name}.png")
        with dpg.texture_registry(show=False):
           dpg.add_static_texture(width=width, height=height, default_value=data, tag=f"texture_{name}")
        initedPIC.append(f"texture_{name}")

with dpg.font_registry():
    font0 = dpg.add_font(file="My.otf", size=12)
    font01 = dpg.add_font(file="My.otf", size=14)
    font1 = dpg.add_font(file="My.otf", size=20)
    font2 = dpg.add_font(file="My.otf", size=40)
    font3 = dpg.add_font(file="My.otf", size=50)
    font4 = dpg.add_font(file="My.otf", size=60)


with dpg.theme(tag="theme_button_red"):
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (177, 86, 135, 255))
with dpg.theme(tag="theme_button_gr"):
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (51, 51, 55, 255))

with dpg.theme(tag="theme_progressbar_green"):
    with dpg.theme_component(dpg.mvProgressBar):
        dpg.add_theme_color(dpg.mvThemeCol_PlotHistogram, (15, 135, 86, 255))
with dpg.theme(tag="theme_progressbar_blue"):
    with dpg.theme_component(dpg.mvProgressBar):
        dpg.add_theme_color(dpg.mvThemeCol_PlotHistogram, (15, 86, 135, 255))

def TEMPDEBUG(sender, app_data, user_data):
    print(ITEMS,STRUCTURS,CRAFTS,sITEMS,sSTRUCTURS,sCRAFTS,TEMPID,sLevel,sFather,sLinks,NODES, sep="\n")

def buttonhelp(sender, app_data, user_data):
    import webbrowser
    url = "https://vk.com/degroidnayatvarina"
    webbrowser.open(url, new=0, autoraise=True)

with dpg.window(no_resize=True, tag="Main_window"):
    with dpg.group():
        with dpg.group(horizontal=True):
            dpg.add_loading_indicator(circle_count=12, style=0, radius=7, speed=0.3)
            dpg.bind_item_font(dpg.add_text(default_value="Satisfactory\ncalculator"), font3)
            dpg.add_button(label="Debag", width=171, callback=TEMPDEBUG, show=False) #Button debug
        with dpg.group(horizontal=True, horizontal_spacing=5):
            dpg.bind_item_font(dpg.add_button(label="Help", width=171, callback=buttonhelp), font1)
            dpg.bind_item_font(dpg.add_combo((), width=387, default_value="Select item: ", tag="Combobox"), font1)
            dpg.bind_item_font(dpg.add_button(label="Clear", width=98, callback=clear_node), font1)
        dpg.add_separator()
        with dpg.group(horizontal=True, horizontal_spacing=5):
            with dpg.group():
                from os.path import isfile
                try:
                    import shutil
                    shutil.rmtree("TEMP")
                except:
                    pass
                if isfile("BD.xlsx"):
                    _ = 1.0
                    DBget()
                    ListComboboxVar.set(convertDictList(sITEMS))
                else:
                    _ = 0.0
                dpg.add_progress_bar(tag="Download", default_value=_, width=346, height=3)
                dpg.bind_item_theme("Download", "theme_progressbar_green")
                with dpg.group(horizontal=True, horizontal_spacing=5):
                    dpg.bind_item_font(dpg.add_button(tag="DB1", label=" Data Update ", width=171, height=49, callback=update_data), font1)
                    dpg.bind_item_font(dpg.add_button(tag="DB2", label=" Clear Data ", width=170, height=49, callback=clear_data), font1)

            dpg.bind_item_font(dpg.add_button(label="Calculate", tag="Calculate", width=315, height=56, callback=START_CRAFT), font2)

        with dpg.node_editor(
                callback=lambda sender, app_data: dpg.add_node_link(app_data[0], app_data[1], parent=sender),
                delink_callback=lambda sender, app_data: dpg.delete_item(app_data), minimap=True,
                minimap_location=dpg.mvNodeMiniMap_Location_BottomRight, tag="node_editor"):
            pass
dpg.set_primary_window(window="Main_window", value=True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()