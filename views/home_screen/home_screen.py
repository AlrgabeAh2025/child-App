import qrcode, base64, requests
from io import BytesIO
from flet import *
import asyncio



class Home(View):
    def __init__(self, route, page):
        super().__init__(route=route)
        self.scroll = ScrollMode.HIDDEN
        self.page = page
        self.screenShotState = False

        self.drawer = NavigationDrawer(
            on_change=self.handle_change,
            controls=[
                Container(height=12),
                NavigationDrawerDestination(
                    label="الرئيسية",
                    icon_content=Icon(icons.HOME_OUTLINED),
                    selected_icon_content=Icon(icons.HOME),
                ),
                NavigationDrawerDestination(
                    label="تسجيل الخروج",
                    icon_content=Icon(icons.LOGOUT_OUTLINED),
                    selected_icon_content=Icon(icons.LOGOUT),
                ),
            ],
        )

        self.appbar = AppBar(
            actions=[
                IconButton(
                    icon=icons.PERSON,
                    icon_color="#ffffff",
                    on_click=lambda x: self.page.go("/Profile"),
                ),
            ],
            leading=IconButton(
                icon=icons.MENU,
                icon_color="#ffffff",
                on_click=lambda e: self.page.open(self.drawer),
            ),
            toolbar_height=100,
            title=Text(
                "حماية الاطفال",
                size=20,
                weight=FontWeight.BOLD,
                color="#ffffff",
                font_family="ElMessiri",
            ),
        )

    def copy(self, data):
        self.page.set_clipboard(data)
        self.page.open(SnackBar(Text("تم نسخ المفتاح"), open=True))
        self.page.update()

    def hasNoFather(self):
        self.scroll = ScrollMode.ALWAYS
        userData = self.page.client_storage.get("userData")
        qr = self.generateQr(userData)
        self.controls.clear()
        self.controls.append(
            ResponsiveRow(
                controls=[
                    Container(
                        content=Column(
                            controls=[
                                ListTile(
                                    leading=Icon(icons.INFO),
                                    title=Text(
                                        "امسح رمز (QR) بالاسفل للاقتران بهاذة الجهاز",
                                        size=13,
                                        weight=FontWeight.NORMAL,
                                        color="#666666",
                                        font_family="ElMessiri",
                                    ),
                                ),
                                Container(
                                    content=Text(
                                        "اولا يجب ان تقوم بإنشاء حساب في هاتف الاب ثم يمكنك مسح رمز (QR) بالاسفل للاقتران مع هذا الجهاز",
                                        size=13,
                                        weight=FontWeight.NORMAL,
                                        color="#666666",
                                        font_family="ElMessiri",
                                    ),
                                    padding=10,
                                ),
                            ]
                        ),
                        bgcolor="#ffffff",
                        border=border.all(color="#110b22", width=1),
                        border_radius=border_radius.all(10),
                    ),
                    Container(height=10),
                    Container(
                        content=Text(
                            "ادخل هذا في هاتف الاب للأقتران بالجهاز",
                            size=13,
                            weight=FontWeight.NORMAL,
                            color="#666666",
                            font_family="ElMessiri",
                        ),
                    ),
                    Container(
                        content=ListTile(
                            title=Text(
                                f"{userData['key']}",
                                style=TextStyle(
                                    size=11,
                                    weight=FontWeight.BOLD,
                                    font_family="ElMessiri",
                                ),
                            ),
                            trailing=IconButton(
                                icon=icons.COPY,
                            ),
                        ),
                        bgcolor="#ffffff",
                        border=border.all(0.5, "#110b22"),
                        border_radius=border_radius.all(5),
                        on_click=lambda x: self.copy(f"{userData['key']}"),
                    ),
                    Container(height=10),
                    Container(
                        content=Text(
                            "أو إمسح رمز (QR) للحصول على المفتاح",
                            size=13,
                            weight=FontWeight.NORMAL,
                            color="#666666",
                            font_family="ElMessiri",
                        ),
                    ),
                    Container(
                        content=Column(
                            controls=[
                                Image(src_base64=qr, width=200),
                                Container(
                                    content=Text(
                                        "امسح رمز (QR)",
                                        size=14,
                                        weight=FontWeight.NORMAL,
                                        color="#666666",
                                        font_family="ElMessiri",
                                    ),
                                ),
                            ],
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            alignment=MainAxisAlignment.CENTER,
                        ),
                        bgcolor="#ffffff",
                        border=border.all(color="#110b22", width=1),
                        border_radius=border_radius.all(10),
                        padding=padding.symmetric(vertical=10),
                    ),
                ],
                expand=True,
            )
        )
        self.update()

    def hasFatherScreen(self):
        self.controls.clear()
        self.controls.append(
            ResponsiveRow(
                controls=[
                    Container(height=10),
                    Column(
                        controls=[
                            Container(
                                content=Image(src="images/father.png", width=150),
                                # border_radius=border_radius.all(150),
                            ),
                            Container(
                                content=Text(
                                    "اسم الاب",
                                    size=20,
                                    weight=FontWeight.BOLD,
                                    color="#666666",
                                    font_family="ElMessiri",
                                ),
                            ),
                            Container(height=20),
                            ResponsiveRow(
                                controls=[
                                    Text(
                                        "البيانات التي يتم مر اقبتها",
                                        style=TextStyle(
                                            size=12,
                                            weight=FontWeight.BOLD,
                                            font_family="ElMessiri",
                                        ),
                                        color="#666666",
                                        text_align=TextAlign.START,
                                    ),
                                ],
                            ),
                            Container(
                                content=ResponsiveRow(
                                    controls=[
                                        ListTile(
                                            title=Text(
                                                "مراقبة استخدام التطبيقات",
                                                style=TextStyle(
                                                    size=14,
                                                    weight=FontWeight.BOLD,
                                                    font_family="ElMessiri",
                                                ),
                                            ),
                                            trailing=Switch(
                                                value=False,
                                                active_color="#110b22",
                                                on_change=self.startGetScreenShot
                                            ),
                                            subtitle=Text(
                                                "مغلق",
                                                style=TextStyle(
                                                    size=10,
                                                    weight=FontWeight.BOLD,
                                                    font_family="ElMessiri",
                                                ),
                                            ),
                                        ),
                                    ],
                                ),
                                bgcolor="#ffffff",
                                border=border.all(0.5, "#110b22"),
                                border_radius=border_radius.all(5),
                                alignment=alignment.center,
                            ),
                            Container(
                                content=ResponsiveRow(
                                    controls=[
                                        ListTile(
                                            title=Text(
                                                "مراقبة الشاشة",
                                                style=TextStyle(
                                                    size=14,
                                                    weight=FontWeight.BOLD,
                                                    font_family="ElMessiri",
                                                ),
                                            ),
                                            trailing=Switch(
                                                value=False,
                                                active_color="#110b22",
                                            ),
                                            subtitle=Text(
                                                "مغلق",
                                                style=TextStyle(
                                                    size=10,
                                                    weight=FontWeight.BOLD,
                                                    font_family="ElMessiri",
                                                ),
                                            ),
                                        ),
                                    ],
                                ),
                                bgcolor="#ffffff",
                                border=border.all(0.5, "#110b22"),
                                border_radius=border_radius.all(5),
                                alignment=alignment.center,
                            ),
                            Container(height=20),
                            ResponsiveRow(
                                controls=[
                                    Text(
                                        "ايقاف عمل التطبيق",
                                        style=TextStyle(
                                            size=12,
                                            weight=FontWeight.BOLD,
                                            font_family="ElMessiri",
                                        ),
                                        color="#666666",
                                        text_align=TextAlign.START,
                                    ),
                                ],
                            ),
                            ResponsiveRow(
                                controls=[
                                    Container(
                                        content=ListTile(
                                            title=Text(
                                                "الغاء الربط مع هاتف الاب",
                                                style=TextStyle(
                                                    size=15,
                                                    weight=FontWeight.BOLD,
                                                    font_family="ElMessiri",
                                                ),
                                            ),
                                            trailing=IconButton(
                                                icon=icons.CANCEL,
                                            ),
                                        ),
                                        bgcolor="#ffffff",
                                        border=border.all(0.5, "#110b22"),
                                        border_radius=border_radius.all(10),
                                    ),
                                ],
                            ),
                        ],
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        alignment=MainAxisAlignment.CENTER,
                    ),
                ],
                expand=True,
            )
        )
        self.update()

    def did_mount(self):
        self.loaderUi()
        self.checkIsThereFather()

    def generateQr(self, userData):
        qrCode = qrcode.make(f"{userData['key']}")
        buffered = BytesIO()

        qrCode.save(buffered, format="PNG")
        sl = base64.b64encode(buffered.getvalue())
        resultOfQr = sl.decode("utf-8")
        return resultOfQr

    async def sendHeadRequest(self, url, body={}):
        access = await self.page.client_storage.get_async("access")
        headers = {
            "Authorization": f"Bearer {access}",
            "Accept": "*/*",
            "Cache-Control": "no-cache",
        }
        try:
            response = requests.head(
                url=f"{Home.baseUrl}/{url}/", data=body, headers=headers
            )
            if response.status_code == 200:
                return [True, "has"]
            else:
                return [False, "hasNo"]
        except requests.exceptions.Timeout:
            return [False, "اتصال الانترنت بطئ"]
        except requests.exceptions.ConnectionError:
            return [False, "حدث خطأ في الاتصال بالخادم. تحقق من اتصالك بالإنترنت."]

    def showMessage(self, message):
        snack_bar = SnackBar(
            content=Text(
                f"{message}",
                style=TextStyle(size=15, font_family="ElMessiri"),
            ),
            show_close_icon=True,
        )
        self.page.open(snack_bar)

    async def getBackground(self):
        while self.screenShotState:
            try:
                requests.get("https://www.google.com", timeout=5)
            except requests.exceptions.ConnectionError:
                await asyncio.sleep(5)  
                continue  

            try:
                response = requests.get("http://localhost:8080/screenshot")
                if response.status_code == 200:
                    files = {"file": ("screenshot.png", response.content, "image/png")}
                    upload_response = requests.put(f"{Home.baseUrl}/Analysis/", files=files)

                    if upload_response.status_code == 200:
                        print("✅ تم رفع الصورة بنجاح")
                    else:
                        print(f"⚠️ خطأ أثناء رفع الصورة: {upload_response.text}")
                else:
                    print("❌ لم يتم التقاط لقطة الشاشة بنجاح")

            except requests.exceptions.RequestException as e:
                print(f"⚠️ خطأ في الطلب: {e}")

            if not self.screenShotState:
                break

            await asyncio.sleep(5)  

    def startGetScreenShot(self, stateus):
        if stateus.data == 'true':
            if not self.screenShotState:  
                self.screenShotState = True
                self.page.run_task(self.getBackground)  
                self.showMessage("✅ تم البدء في التقاط الشاشة")
        else:
            self.screenShotState = False  # إيقاف العملية
            self.showMessage("⏹️ تم إيقاف التقاط الشاشة")

    def loaderUi(self):
        self.scroll = None
        self.controls.clear()
        self.controls.append(
            Column(
                controls=[
                    Container(
                        content=ProgressRing(visible=True),  # Progress ring loader
                        alignment=alignment.center,
                        height=float("inf"),  # Make the container take full height
                        expand=True,  # Ensure the container expands to fill available space
                    ),
                ],
                expand=True,  # Make the column expand to take up all available space
            )
        )
        self.update()

    def handle_change(self, e):
        routs = {
            "0": "/home",
            "1": "/",
        }
        if routs[e.data] == "/":
            self.page.client_storage.clear()
        self.page.go(routs[e.data])
        self.page.close(self.drawer)

    def checkIsThereFather(self):
        state, result = self.page.run_task(self.sendHeadRequest, "Children").result()
        if not state:
            self.hasNoFather()
        else:
            self.hasFatherScreen()
