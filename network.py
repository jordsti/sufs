__author__ = 'JordSti'
import random
import re

packet_seed = random.randint(0, 100000)
packet_iterator = 0


def get_packet_id():
    global packet_seed
    global packet_iterator
    packet_id = packet_iterator + packet_seed
    packet_iterator += 1
    return packet_id


class packet_header:
    (Request, Command, FileInformation, FileBlock) = (0, 1, 2, 3) #todo !?!

    def __init__(self, data=None, packet_type=Request):
        self.packet_id = -1
        self.packet_type = packet_type
        self.fields = {}
        self.length = 0

        if data is not None:
            self.__parse_data(data)
        else:
            self.packet_id = get_packet_id()

    def __parse_data(self, data):
        pattern = re.compile("\\[Header:(?P<id>[0-9]+):(?P<type>[0-9]+):(?P<length>[0-9])\\]\\((?P<fields>.*)\\)")

        m = pattern.match(data)

        if m:
            self.packet_id = int(m.group("id"))
            self.packet_type = int(m.group("type"))
            self.length = int(m.group("length"))

            fields = m.group("fields")

            for f in fields.split(';'):
                fdata = f.split(':')
                if len(fdata) == 2:
                    key = fdata[0]
                    val = fdata[1]
                    self.fields[key] = val

        else:
            #todo raise an exception for bad packet
            pass

    def to_chunk(self):
        fdata = ""
        for k in self.fields:
            fdata += "%s:%s;" % (k, self.fields[k])

        fdata = fdata.rstrip(';')

        data = "[Header:%d:%d:%d](%s)" % (self.packet_id, self.packet_type, self.length, fdata)

        return data

class packet:

    def __init__(self, data=None):
        self.header = None
        self.bytes = None
        if data is not None:
            packet_data = data.split('|', 1)
            if len(packet_data) == 1:
                #header only
                self.header = packet_header(packet_data[0])
            elif len(packet_data) == 2:
                self.header = packet_header(packet_data[0])
                if len(packet_data[1]) > 0:
                    self.bytes = packet_data[1]

    def to_string(self):
        txt = "Packet\n"
        txt += "\tHeader { Id : %d, Length : %d, Type : %d }\n" % (self.header.packet_id, self.header.length, self.header.packet_type)
        for f in self.header.fields:
            txt += "Header Fields { %s : %s }\n" % (f, self.header.fields[f])
        if self.bytes is not None:
            txt += "Data\n"
            txt += self.bytes + '\n'
        return txt

    def to_chunk(self):
        if self.bytes is not None:
            return self.header.to_chunk() + "|" + self.bytes
        else:
            return self.header.to_chunk()