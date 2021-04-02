import datetime
import pathlib
import os

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.image import Image as CoreImage
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.config import Config
from kivy.lang import Builder
import base64

import scard
import requests


api_url = 'http://localhost:8080/api/0.1/'
# api_url = 'https://dustpath.in.th/api/0.1/'


font_path = str(
        (pathlib.Path(__file__).resolve().parent /
            'fonts').resolve())
# print(font_path)

Config.set(
        'kivy',
        'default_font', [
            'THSarabunNew',
            font_path + '/THSarabunNew.ttf',
            font_path + '/THSarabunNew Italic.ttf',
            font_path + '/THSarabunNew Bold.ttf',
            font_path + '/THSarabunNew BoldItalic.ttf',
            ])
Config.set('graphics', 'window_state', 'maximized')
Config.set('graphics', 'minimum_width', 1000)
Config.set('graphics', 'minimum_height', 600)

Config.write()

token = {}

def refresh_token():
    global token

    print('Refresh token')

    headers = {
            'Authorization': 'Bearer {}'.format(token['refresh_token'])
            }

    response = requests.post('{}auth/refresh'.format(api_url), headers=headers)
    code = response.status_code
    if code != 200:
        return

    data = response.json()
    token['access_token'] = data.get('access_token', '')


def register(data):
    headers = {
            'Authorization': 'Bearer {}'.format(token['access_token'])
            }

    try:
        response = requests.post(
                '{}gardeners/'.format(api_url),
                json=data,
                headers=headers
            )
    except Exception as e:
        print(e)

        popup = Popup(
                title='ไม่สามารถติดต่อระบบได้',
                content=Label(
                        text='ไม่สามารถติดต่อระบบได้',
                        font_size=35),
                      size_hint=(.6, .6))
        popup.open()

    return response


class AppPopup(Popup):
    message = StringProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class LoginScreen(Screen):
    def login(self):
        global token
        print('API URL', api_url)
        print('Login', self.ids.username.text, self.ids.password.text)
        data = dict(
                username=self.ids.username.text.strip(),
                secret=self.ids.password.text.strip()
                )
        try:
            response = requests.post('{}auth/'.format(api_url), json=data)
        except requests.exceptions.RequestException as e:
            print('error', e)
            self.ids.login_message.text = 'ติดค่อเซิร์ฟเวอร์ไม่ได้'
            return
        except Exception as e:
            print('error', e)
            self.ids.login_message.text = 'เกิดข้อผิดพลาด'
            return
        response = response.json()
        if 'message' in response:
            self.ids.login_message.text = response['message']

        if 'access_token' in response:
            token = response
            self.manager.current = 'register'

    def reset(self):
        self.ids.username.text = ''
        self.ids.password.text = ''


class RegisterScreen(Screen):

    def read_id_card(self):
        reader = None
        try:
            reader = scard.ThaiSmartCardReader()
        except Exception as e:
            print(e)
            popup = AppPopup(
                    title='Cannot Read This Card',
                    title_size=35,    
                    message= 'ไม่สามารถอ่านข้อมูลได้',
                    size_hint=(.6, .6),
                    )
            popup.open()
            return

        thai_name = reader.get_thai_name()
        self.ids.title_input.text = thai_name[0]
        self.ids.firstname_input.text = thai_name[1]
        self.ids.lastname_input.text = thai_name[-1]
        self.ids.id_input.text = reader.get_id()

        birthday = reader.get_date_of_birth()
        self.ids.birth_input.text = '{}/{}/{}'.format(*birthday)
        self.ids.gender_input.text = reader.get_gender()
        address = reader.get_address()
        self.ids.address_number.text = address[0]
        self.ids.address_moo.text = address[1]
        self.ids.address_alleyway.text = address[2].replace('ตรอก', '')
        self.ids.address_alley.text = address[3].replace('ซอย', '')
        self.ids.address_street.text = address[4].replace('ถนน', '')
        self.ids.address_subdistrict.text = address[5].replace('ตำบล', '')
        self.ids.address_district.text = address[6].replace('อำเภอ', '')
        self.ids.address_province.text = address[7].replace('จังหวัด', '')

        self.imageio = None
        self.imageio = reader.get_photo()
        self.coreimage = CoreImage(self.imageio, ext="jpg")
        self.ids.gardener_image.texture = self.coreimage.texture
        
        self.ids.document_copy_of_id_card.active = True
        self.ids.document_copy_of_bankbook.active = True
        self.ids.document_land_rights_documents.active = True
        self.ids.document_gap_certificaiton_documents.active = True
        self.ids.gardener_new.active = True

    def register(self):
        global token
        if not token:
            self.root.manager.current = 'login'
            return

        blist = [int(d) for d in self.ids.birth_input.text.split('/')]
        blist[-1] -= 543
        blist.reverse()

        try:
            photo=base64.b64encode(self.imageio.getvalue()).decode('utf-8')
        except Exception as e:
            print(e)
            popup = AppPopup(
                    title='Cannot Read Photo Card',
                    title_size=35,    
                    message= 'ไม่สามารถอ่านรูปได้',
                    size_hint=(.6, .6),
                    )
            popup.open()
            return

        data = dict(
                citizen_id=self.ids.id_input.text,
                title=self.ids.title_input.text,
                firstname=self.ids.firstname_input.text,
                lastname=self.ids.lastname_input.text,
                birthday=datetime.date(
                    *blist).isoformat(),
                gender=self.ids.gender_input.text,
                phone=self.ids.phone.text,
                photo=photo,
                address=dict(
                    number=self.ids.address_number.text,
                    moo=self.ids.address_moo.text,
                    alleyway=self.ids.address_alleyway.text,
                    alley=self.ids.address_alley.text,
                    street=self.ids.address_street.text,
                    subdistrict=self.ids.address_subdistrict.text,
                    district=self.ids.address_district.text,
                    province=self.ids.address_province.text,
                    postcode=self.ids.address_postcode.text
                    ),
                documents=dict(
                    copy_of_id_card=self.ids.document_copy_of_id_card.active,
                    copy_of_bankbook=self.ids.document_copy_of_bankbook.active,
                    land_rights_documents=self.ids.document_land_rights_documents.active,
                    gap_certificaiton_documents=self.ids.document_gap_certificaiton_documents.active,
                    )
                )
        status_text = ['รายใหม่', 'รายเดิม', 'รายเดิม (อุทธรณ์)']
        status_ids = [self.ids.gardener_new,
                      self.ids.gardener_old,
                      self.ids.gardener_old_appeal]

        for status_text, status_id in zip(status_text, status_ids):
            if status_id.active:
                status = status_text
                break
        data['status'] = status
        # print('infomation: ', data)

        response = register(data)
        if response.status_code == 401:
            refresh_token()
            response = register(data)
            if response.status_code == 401:
                self.manager.current = 'login'
                popup = AppPopup(
                        title='ระยะเวลาที่ใช้งานเกินกำหนด กรุณา login ใหม่',
                        message='ระยะเวลาที่ใช้งานเกินกำหนด กรุณา login ใหม่',
                        title_size=35,
                        size_hint=(.8, .8),
                        )
                popup.open()
                return

        try:
            data = response.json()
        except Exception as e:
            print(e)
            popup = AppPopup(
                    title='ไม่สามารถบันทึกข้อมูลได้',
                    message='ข้อมูลคุณ {} ไม่สามารถบันทึกได้ กรุณาใช้เว็บในการบันทึกข้อมูล'.format(
                                self.ids.firstname_input.text,
                                ),
                    title_size=35,
                    size_hint=(.6, .6),
                    )
            popup.open()
            return


        if 'result' in data and data['result'] == 'save':
            popup = AppPopup(
                    title='บันทึกข้อมูลเรียบร้อยแล้ว',
                    message='บันทึกข้อมูลคุณ {} เรียบร้อยแล้ว\nรหัสเกษตรกรคือ {}\nMessage: {}'.format(
                                self.ids.firstname_input.text,
                                data['code'],
                                data['message']
                                ),
                    title_size=35,
                    size_hint=(.6, .6),
                    )
            popup.open()

        else:
            text = 'เกษตรกรท่านนี้ไม่สามารถลงทะเบียนได้ กรุณาตรวจสอบในระบบ\n{}'
            if 'message' in data:
                text = text.format(
                    data.get('message', '')
                    )
            popup = AppPopup(
                    title='ไม่สามารถลงทะเบียนได้',
                    message=text,
                    title_size=35,
                    size_hint=(.8, .8),
                    )
            popup.open()


class MongthongScreenManager(ScreenManager):
    pass


class MonthongApp(App):
    def build(self):
        kv_path = str((pathlib.Path(__file__).resolve().parent / 'monthong_app.kv').resolve())
        with open(kv_path, encoding='utf8') as f: 
            Builder.load_string(f.read())
        return MongthongScreenManager()


if __name__ == '__main__':
    # global api_url

    debug = os.getenv('MONTHONG_DEBUG')
    if type(debug) is str:
        debug = True if debug.lower() == 'true' else False
    else:
        debug = False

    if debug:
        print('Run in debug mode')
        api_url = 'http://localhost:8080/api/0.1/'
    MonthongApp().run()
