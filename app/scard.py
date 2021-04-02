#  install pcscd python-pyscard python-pil
from PIL import Image
from smartcard.System import readers
from smartcard.util import HexListToBinString, toHexString, toBytes


# Check card
SELECT = [0x00, 0xA4, 0x04, 0x00, 0x08]
THAI_CARD = [0xA0, 0x00, 0x00, 0x00, 0x54, 0x48, 0x00, 0x01]

# CID
CMD_CID = [0x80, 0xb0, 0x00, 0x04, 0x02, 0x00, 0x0d]

# TH Fullname
CMD_THFULLNAME = [0x80, 0xb0, 0x00, 0x11, 0x02, 0x00, 0x64]

# EN Fullname
CMD_ENFULLNAME = [0x80, 0xb0, 0x00, 0x75, 0x02, 0x00, 0x64]

# Date of birth
CMD_BIRTH = [0x80, 0xb0, 0x00, 0xD9, 0x02, 0x00, 0x08]

# Gender
CMD_GENDER = [0x80, 0xb0, 0x00, 0xE1, 0x02, 0x00, 0x01]

# Card Issuer
CMD_ISSUER = [0x80, 0xb0, 0x00, 0xF6, 0x02, 0x00, 0x64]

# Issue Date
CMD_ISSUE = [0x80, 0xb0, 0x01, 0x67, 0x02, 0x00, 0x08]

# Expire Date
CMD_EXPIRE = [0x80, 0xb0, 0x01, 0x6F, 0x02, 0x00, 0x08]

# Address
CMD_ADDRESS = [0x80, 0xb0, 0x15, 0x79, 0x02, 0x00, 0x64]

# Photo_Part1/20
CMD_PHOTO1 = [0x80, 0xb0, 0x01, 0x7B, 0x02, 0x00, 0xFF]
# Photo_Part2/20
CMD_PHOTO2 = [0x80, 0xb0, 0x02, 0x7A, 0x02, 0x00, 0xFF]
# Photo_Part3/20
CMD_PHOTO3 = [0x80, 0xb0, 0x03, 0x79, 0x02, 0x00, 0xFF]
# Photo_Part4/20
CMD_PHOTO4 = [0x80, 0xb0, 0x04, 0x78, 0x02, 0x00, 0xFF]
# Photo_Part5/20
CMD_PHOTO5 = [0x80, 0xb0, 0x05, 0x77, 0x02, 0x00, 0xFF]
# Photo_Part6/20
CMD_PHOTO6 = [0x80, 0xb0, 0x06, 0x76, 0x02, 0x00, 0xFF]
# Photo_Part7/20
CMD_PHOTO7 = [0x80, 0xb0, 0x07, 0x75, 0x02, 0x00, 0xFF]
# Photo_Part8/20
CMD_PHOTO8 = [0x80, 0xb0, 0x08, 0x74, 0x02, 0x00, 0xFF]
# Photo_Part9/20
CMD_PHOTO9 = [0x80, 0xb0, 0x09, 0x73, 0x02, 0x00, 0xFF]
# Photo_Part10/20
CMD_PHOTO10 = [0x80, 0xb0, 0x0A, 0x72, 0x02, 0x00, 0xFF]
# Photo_Part11/20
CMD_PHOTO11 = [0x80, 0xb0, 0x0B, 0x71, 0x02, 0x00, 0xFF]
# Photo_Part12/20
CMD_PHOTO12 = [0x80, 0xb0, 0x0C, 0x70, 0x02, 0x00, 0xFF]
# Photo_Part13/20
CMD_PHOTO13 = [0x80, 0xb0, 0x0D, 0x6F, 0x02, 0x00, 0xFF]
# Photo_Part14/20
CMD_PHOTO14 = [0x80, 0xb0, 0x0E, 0x6E, 0x02, 0x00, 0xFF]
# Photo_Part15/20
CMD_PHOTO15 = [0x80, 0xb0, 0x0F, 0x6D, 0x02, 0x00, 0xFF]
# Photo_Part16/20
CMD_PHOTO16 = [0x80, 0xb0, 0x10, 0x6C, 0x02, 0x00, 0xFF]
# Photo_Part17/20
CMD_PHOTO17 = [0x80, 0xb0, 0x11, 0x6B, 0x02, 0x00, 0xFF]
# Photo_Part18/20
CMD_PHOTO18 = [0x80, 0xb0, 0x12, 0x6A, 0x02, 0x00, 0xFF]
# Photo_Part19/20
CMD_PHOTO19 = [0x80, 0xb0, 0x13, 0x69, 0x02, 0x00, 0xFF]
# Photo_Part20/20
CMD_PHOTO20 = [0x80, 0xb0, 0x14, 0x68, 0x02, 0x00, 0xFF]


class ThaiSmartCardReader:
    def __init__(self):
        # Get all the available readers
        readerList = readers()
        print('Available readers:')
        for readerIndex, readerItem in enumerate(readerList):
            print(readerIndex, readerItem)

        # Select reader
        readerSelectIndex = 0  # int(input('Select reader[0]: ') or '0')
        reader = readerList[readerSelectIndex]

        print('Using:', reader)
        self.connection = reader.createConnection()
        self.connection.connect()
        atr = self.connection.getATR()

        print('ATR: ' + toHexString(atr))
        if (atr[0] == 0x3B & atr[1] == 0x67):
            self.req = [0x00, 0xc0, 0x00, 0x01]
        else:
            self.req = [0x00, 0xc0, 0x00, 0x00]

        # Check card
        data, sw1, sw2 = self.connection.transmit(SELECT + THAI_CARD)
        print('Select Applet: %02X %02X' % (sw1, sw2))

        self.PHOTO = [
            CMD_PHOTO1, CMD_PHOTO2, CMD_PHOTO3, CMD_PHOTO4, CMD_PHOTO5,
            CMD_PHOTO6, CMD_PHOTO7, CMD_PHOTO8, CMD_PHOTO9, CMD_PHOTO10,
            CMD_PHOTO11, CMD_PHOTO12, CMD_PHOTO13, CMD_PHOTO14, CMD_PHOTO15,
            CMD_PHOTO16, CMD_PHOTO17, CMD_PHOTO18, CMD_PHOTO19, CMD_PHOTO20]

    def decode(self, data):
        result = bytes(data).decode('tis-620')
        return result.strip()

    def get_data(self, cmd, req=[0x00, 0xc0, 0x00, 0x00]):
        data, sw1, sw2 = self.connection.transmit(cmd)
        data, sw1, sw2 = self.connection.transmit(req + [cmd[-1]])
        return [data, sw1, sw2]

    def get_id(self):
        # CID
        data = self.get_data(CMD_CID, self.req)
        cid = self.decode(data[0])
        print('CID: ', cid)
        return cid

    def get_test(self):
        x = [0x80, 0xb0, 0x00, 0xe1, 0x02, 0x00, 0xff]
        data = self.get_data(x, self.req)
        print('=>', data[0], 'x', len(data[0]))
        cid = self.decode(data[0])
        print('CID: ', cid)


    def get_thai_name_raw(self):
        # TH Fullname
        data = self.get_data(CMD_THFULLNAME, self.req)
        name = self.decode(data[0])
        # print('TH Fullname:', name)
        return name

    def get_thai_name(self):
        name = self.get_thai_name_raw()
        return name.split('#')

    def get_english_name(self):
        # EN Fullname
        data = self.get_data(CMD_ENFULLNAME, self.req)
        name = self.decode(data[0])
        print('EN Fullname:', name)
        return name

    def get_date_of_birth(self):
        # Date of birth
        data = self.get_data(CMD_BIRTH, self.req)
        dob = self.decode(data[0])
        print('Date of birth:', dob)
        birthday = (dob[-2:],
                    dob[4:6],
                    dob[:4])

        return birthday

    def get_gender_raw(self):
        # Gender
        data = self.get_data(CMD_GENDER, self.req)
        gender = self.decode(data[0])
        print('Gender:', gender)
        return gender

    def get_gender(self):
        gen_id = self.get_gender_raw()
        genders = ['ชาย', 'หญิง']
        return genders[int(gen_id)-1]

    def get_card_issuer(self):
        # Card Issuer
        data = self.getData(CMD_ISSUER, self.req)
        issuer = self.decode(data[0])
        print('Card Issuer:', issuer)
        return issuer

    def get_issue_date(self):
        # Issue Date
        data = self.get_data(CMD_ISSUE, self.req)
        issue_date = self.decode(data[0])
        print('Issue Date:', issue_date)

    def get_expired_date(self):
        # Expire Date
        data = self.get_data(CMD_EXPIRE, self.req)
        expired_date = self.decode(data[0])
        print('Expire Date:', expired_date)
        return expired_date

    def get_address_raw(self):
        # Address
        data = self.get_data(CMD_ADDRESS, self.req)
        address = self.decode(data[0])
        # print('Address:', address)
        return address

    def get_address(self):
        data = self.get_address_raw()
        return data.split('#')

    def get_photo(self):
        import io
        data = []
        for d in self.PHOTO:
            response, sw1, sw2 = self.connection.transmit(d)
            if sw1 == 0x61:
                GET_RESPONSE = [0X00, 0XC0, 0x00, 0x00]
                apdu = GET_RESPONSE + [sw2]
                response, sw1, sw2 = self.connection.transmit(apdu)
                data.extend(response)

        imageio = io.BytesIO(bytearray(data))
        return imageio

    def save_photo(self, filename):
        fphoto = open('{}.jpg'.format(filename), 'wb')
        for d in self.PHOTO:
            response, sw1, sw2 = self.connection.transmit(d)
            if sw1 == 0x61:
                GET_RESPONSE = [0X00, 0XC0, 0x00, 0x00]
                apdu = GET_RESPONSE + [sw2]
                response, sw1, sw2 = self.connection.transmit(apdu)
                fphoto.write(bytearray(response))


if __name__ == '__main__':
    reader = ThaiSmartCardReader()
    print(reader.get_test())
