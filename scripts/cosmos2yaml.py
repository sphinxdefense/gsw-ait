import sys
import yaml
import shlex

endianess = "LSB"
cosmos2ait_types = {
    "8 UINT": "U8",
    "64 FLOAT": f"{endianess}_D64",
    "32 FLOAT": f"{endianess}_F32",
    "32 UINT": f"{endianess}_U32",
    "32 INT": f"{endianess}_I32",
    "16 UINT": f"{endianess}_U16",
    "64 UINT": f"{endianess}_U64",
    "16 INT": f"{endianess}_I16",
}

type2bytes = {
    "U8": 1,
    f"{endianess}_D64": 8,
    f"{endianess}_F32": 4,
    f"{endianess}_U32": 4,
    f"{endianess}_I32": 4,
    f"{endianess}_U16": 2,
    f"{endianess}_U64": 8,
    f"{endianess}_I16": 2,
}


class Packet(yaml.YAMLObject):
    yaml_tag = "!Packet"

    def __init__(self, name, fields):
        self.name = name
        self.fields = fields

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, fields={self.fields})"


class Field(yaml.YAMLObject):
    yaml_tag = "!Field"

    def __init__(self, name, desc, type, bytes=None, enum=None):
        self.name = name
        self.desc = desc
        self.type = type
        if enum is None:
            self.enum = {}
        self.bytes = bytes

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, desc={self.desc} type={self.type} enum={self.enum})"


def main(args):
    fn = args[0]
    with open(fn, mode="r") as f:
        lines = f.readlines()
        cur_write_fn = None
        cur_yaml = None
        for line in lines:
            words = shlex.split(line)
            if len(words) == 0:
                continue
            if words[0] == "TELEMETRY":
                if cur_write_fn is not None and cur_yaml is not None:
                    print("writing file")
                    yaml.dump(
                        cur_yaml, cur_write_fn, sort_keys=False, default_flow_style=None
                    )
                    cur_write_fn.close()
                pkt_name = words[2]
                cur_write_fn = open(f"{pkt_name}.yaml", "w")
                cur_yaml = Packet(name=pkt_name, fields=[])
                cur_byte = 0
                # cur_yaml = {"name": pkt_name,
                #             "fields": []}
                continue
            if len([w for w in words if "CCSDS_" in w]) == 0:
                if "STRING" in words:
                    cur_yaml.fields.append(
                        Field(
                            name=words[1],
                            desc=(words[4] if len(words) == 5 else words[5]),
                            type="U8",
                            bytes=[cur_byte, cur_byte + int(words[2]) - 1],
                        )
                    )
                    cur_byte += int(words[2])
                    continue
                if words[0] == "STATE":
                    cur_yaml.fields[-1].enum[int(words[-1])] = words[-2]
                else:
                    if len(words) > 4 and words[3] == "BLOCK":
                        continue
                    type = cosmos2ait_types[f"{words[2]} {words[3]}"]
                    cur_byte += type2bytes[type]
                    cur_yaml.fields.append(
                        Field(
                            name=words[1],
                            desc=(words[4] if len(words) == 5 else words[5]),
                            type=type,
                        )
                    )
        print("writing file")
        yaml.dump(cur_yaml, cur_write_fn, sort_keys=False)
        cur_write_fn.close()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
