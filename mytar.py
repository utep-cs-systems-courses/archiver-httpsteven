#!/usr/bin/env python3
import sys

def read_file_contents(filename):
    with open(filename, 'rb') as file:
        return file.read()

def write_file(filename, content):
    with open(filename, 'wb') as file:
        file.write(content)

def archive_outband(archive_path, filenames):
    with open(archive_path, 'wb') as archive:
        for filename in filenames:
            content = read_file_contents(filename)
            header = f"{filename}:{len(content)}:".encode()
            archive.write(header + content)

def extract_outband(archive_path):
    with open(archive_path, 'rb') as archive:
        content = archive.read()
        while content:
            pos = content.find(b':')
            filename, content = content[:pos].decode(), content[pos+1:]
            pos = content.find(b':')
            size, content = int(content[:pos]), content[pos+1:]
            file_content, content = content[:size], content[size:]
            write_file(filename, file_content)

def archive_inband(archive_path, filenames):
    with open(archive_path, 'wb') as archive:
        for filename in filenames:
            content = read_file_contents(filename)
            footer = f"/{filename}:{len(content)}/e".encode()
            archive.write(content + footer)

def extract_inband(archive_path):
    with open(archive_path, 'rb') as archive:
        content = archive.read()

    while content:
        footer_start = content.rfind(b"/", 0, -2)  # Avoid the last "/e"
        if footer_start == -1:
            break
        footer_content = content[footer_start+1:-2].decode()
        filename, size = footer_content.split(':')
        size = int(size)
        file_start = footer_start - size
        file_content = content[file_start:footer_start]
        write_file(filename, file_content)
        content = content[:file_start]

def main():
    if len(sys.argv) < 4:
        print("Usage: mytar.py [i|o] [c|x] [archive_name] [files...]", file=sys.stderr)
        sys.exit(1)

    mode, operation, archive_name = sys.argv[1], sys.argv[2], sys.argv[3]
    files = sys.argv[4:] if operation == 'c' else []

    actions = {
        ('o', 'c'): lambda: archive_outband(archive_name, files),
        ('o', 'x'): lambda: extract_outband(archive_name),
        ('i', 'c'): lambda: archive_inband(archive_name, files),
        ('i', 'x'): lambda: extract_inband(archive_name)
    }

    action = actions.get((mode, operation))
    if action:
        action()
    else:
        print(f"Unknown operation or mode: {operation} {mode}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()#!/usr/bin/env python3
import sys

def read_file_contents(filename):
    with open(filename, 'rb') as file:
        return file.read()

def write_file(filename, content):
    with open(filename, 'wb') as file:
        file.write(content)

def archive_outband(archive_path, filenames):
    with open(archive_path, 'wb') as archive:
        for filename in filenames:
            content = read_file_contents(filename)
            header = f"{filename}:{len(content)}:".encode()
            archive.write(header + content)

def extract_outband(archive_path):
    with open(archive_path, 'rb') as archive:
        content = archive.read()
        while content:
            pos = content.find(b':')
            filename, content = content[:pos].decode(), content[pos+1:]
            pos = content.find(b':')
            size, content = int(content[:pos]), content[pos+1:]
            file_content, content = content[:size], content[size:]
            write_file(filename, file_content)

def archive_inband(archive_path, filenames):
    with open(archive_path, 'wb') as archive:
        for filename in filenames:
            content = read_file_contents(filename)
            footer = f"/{filename}:{len(content)}/e".encode()
            archive.write(content + footer)

def extract_inband(archive_path):
    with open(archive_path, 'rb') as archive:
        content = archive.read()

    while content:
        footer_start = content.rfind(b"/", 0, -2)  # Avoid the last "/e"
        if footer_start == -1:
            break
        footer_content = content[footer_start+1:-2].decode()
        filename, size = footer_content.split(':')
        size = int(size)
        file_start = footer_start - size
        file_content = content[file_start:footer_start]
        write_file(filename, file_content)
        content = content[:file_start]

def main():
    if len(sys.argv) < 4:
        print("Usage: mytar.py [i|o] [c|x] [archive_name] [files...]", file=sys.stderr)
        sys.exit(1)

    mode, operation, archive_name = sys.argv[1], sys.argv[2], sys.argv[3]
    files = sys.argv[4:] if operation == 'c' else []

    actions = {
        ('o', 'c'): lambda: archive_outband(archive_name, files),
        ('o', 'x'): lambda: extract_outband(archive_name),
        ('i', 'c'): lambda: archive_inband(archive_name, files),
        ('i', 'x'): lambda: extract_inband(archive_name)
    }

    action = actions.get((mode, operation))
    if action:
        action()
    else:
        print(f"Unknown operation or mode: {operation} {mode}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()#!/usr/bin/env python3
import sys
import os

def create_archive_outband(archive_path, filenames):
    with open(archive_path, 'wb') as archive:
        for filename in filenames:
            # Use the filename directly in the current directory
            with open(filename, 'rb') as f:
                content = f.read()
                header = f"{filename}:{len(content)}:".encode()
                archive.write(header + content)

def extract_archive_outband(archive_path):
    with open(archive_path, 'rb') as archive:
        content = archive.read()
        while content:
            pos = content.find(b':')
            filename = content[:pos].decode()
            content = content[pos+1:]
            pos = content.find(b':')
            size = int(content[:pos])
            content = content[pos+1:]
            file_content = content[:size]
            content = content[size:]
            # Extract files to the current directory
            with open(filename, 'wb') as f:
                f.write(file_content)

def create_archive_inband(archive_path, filenames):
    with open(archive_path, 'wb') as archive:
        for filename in filenames:
            with open(filename, 'rb') as f:
                content = f.read()
                # Directly write the file size and filename as the footer
                footer = f"/{filename}:{len(content)}/e".encode()
                archive.write(content + footer)

def extract_archive_inband(archive_path):
    with open(archive_path, 'rb') as archive:
        content = archive.read()

    while content:
        # Look for the footer start marker "/"
        footer_start = content.rfind(b"/", 0, -2)  # Search before the last 2 bytes to avoid catching "/e"
        if footer_start == -1:
            break

        # Parse the footer to get filename and size
        footer_content = content[footer_start+1:-2].decode()  # Exclude "/e"
        filename, size = footer_content.split(':')
        size = int(size)

        # Extract the file content based on size
        file_start = footer_start - size
        file_content = content[file_start:footer_start]

        # Write the extracted file
        with open(filename, 'wb') as f:
            f.write(file_content)

        # Update the remaining content
        content = content[:file_start]
                
#Inband Framer and Outband Framer Implementation


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: mytar.py [i|o] [c|x] [archive_name] [files...]", file=sys.stderr)
        sys.exit(1)

    type_extract = sys.argv[1]
    operation = sys.argv[2]
    archive_name = sys.argv[3]  # Use the given path directly without converting to absolute path

    if operation == "c" and type_extract == "o":
        files_to_archive = sys.argv[4:]
        create_archive_outband(archive_name, files_to_archive)
    elif operation == "x" and type_extract == "o":
        extract_archive_outband(archive_name)
    elif operation == "c" and type_extract == "i":
        files_to_archive = sys.argv[4:]
        create_archive_inband(archive_name, files_to_archive)
    elif operation == "x" and type_extract == "i":
        extract_archive_inband(archive_name)
    else:
        print(f"Unknown operation: {operation}", file=sys.stderr)
        sys.exit(1)
