def main():
  command = input("ccwc ")
  option = command.split()[0]
  file_name = command.split()[1]

  try:
    with open(file_name, "r") as file:
      content = file.read()

      if option == "-c":
        print(f"{len(content)} {file_name}")

  except FileNotFoundError:
    print(f"Error: {file_name} was not found")

if __name__ == "__main__":
  main()