import sys
from glob import glob
import shlex

endianess = "LSB"
ait2python_types = {
    "U8": "bytearray",
    f"{endianess}_D64": "float",
    f"{endianess}_F32": "float",
    f"{endianess}_U32": "int",
    f"{endianess}_I32": "int",
    f"{endianess}_U16": "int",
    f"{endianess}_U64": "int",
    f"{endianess}_I16": "int",
}


def main(glob_str):
    write_lines = []
    fns = glob(glob_str)
    for fn in fns:
        with open(fn, mode="r") as f:
            lines = f.readlines()
            pkt_name = shlex.split(lines[1])[-1]
            class_name = "".join(
                x for x in pkt_name.title() if not x.isspace() and x != "_"
            )
            write_lines.append(f"class {class_name}(BaseModel):")
            found_name = False
            found_desc = False
            found_type = False
            for line in lines[2:]:
                if "name:" in line:
                    field_name = shlex.split(line)[-1].lower()
                    found_name = True
                if "desc:" in line:
                    try:
                        field_desc = " ".join(shlex.split(line)[1:])
                    except Exception as e:
                        _ = e
                        field_desc = ""
                    found_desc = True
                if "type:" in line:
                    field_type = ait2python_types[shlex.split(line)[-1]]
                    found_type = True
                if found_name and found_desc and found_type:
                    write_lines.append(
                        f'\t{field_name}: {field_type} = Field(description="{field_desc}")'
                    )
                    found_name = False
                    found_desc = False
                    found_type = False

    with open("schemas.py", "w") as f:
        f.write("\n".join(write_lines))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
