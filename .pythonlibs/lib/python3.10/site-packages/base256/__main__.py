from . import encode, decode, encode_file, decode_file, encode_string, decode_string
from prompt_toolkit.shortcuts import button_dialog, input_dialog, message_dialog
def main():
    if button_dialog(title='Action Chooser', text='What action would you like to perform?', buttons=[('Encode', True), ('Decode', False)]).run():
        # Encode
        encode_type = button_dialog(title='Encode Type', text='What type of encode would you like to perform?', buttons=[('Hex', 0), ('File', 1), ('String', 2)]).run()
        if encode_type == 0:
            # Hex
            output = encode(input_dialog(title='Hex Value', text='What hex value would you like to encode?').run())
            message_dialog(title='Encoded String', text=output).run()
            print(output)
        elif encode_type == 1:
            # File
            output = encode_file(input_dialog(title='File Path', text='What file would you like to encode?').run())
            message_dialog(title='Encoded String', text=output).run()
            print(output)
        elif encode_type == 2:
            # String
            output = encode_string(input_dialog(title='String', text='What string would you like to encode?').run())
            message_dialog(title='Encoded String', text=output).run()
            print(output)
    else:
        # Decode
        decode_type = button_dialog(title='Decode Type', text='What type of decode would you like to perform?', buttons=[('Hex', 0), ('File', 1), ('String', 2)]).run()
        if decode_type == 0:
            # Hex
            output = decode(input_dialog(title='Encoded String', text='What encoded string would you like to decode?').run())
            message_dialog(title='Decoded Hex', text=output).run()
            print(output)
        elif decode_type == 1:
            # File
            decode_file(input_dialog(title='Encoded String', text='What encoded string would you like to decode?').run(), input_dialog(title='File Path', text='What file would you like to decode to?').run())
        elif decode_type == 2:
            # String
            output = decode_string(input_dialog(title='Encoded String', text='What encoded string would you like to decode?').run())
            message_dialog(title='Decoded String', text=output).run()
            print(output)
if __name__ == '__main__':
    main()
