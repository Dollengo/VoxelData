import os
import csv
import hashlib

CSV_FILE = 'database.csv'
ACCOUNTS_FILE = 'accounts.csv'

def create_csv_if_not_exists():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'account_id', 'partition_name', 'chunk_name', 'voxel_index', 'data'])

def create_accounts_csv_if_not_exists():
    if not os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['username', 'password'])

def create_account():
    username = input("Enter username for new account: ")
    password = input("Enter password: ")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()  # Hash da senha
    
    with open(ACCOUNTS_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, hashed_password])
    
    print(f"Account '{username}' created successfully.")

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()  # Hash da senha
    
    with open(ACCOUNTS_FILE, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Pular cabeçalho
        
        for row in reader:
            if len(row) >= 2:  # Verifica se há pelo menos dois elementos na linha
                if row[0] == username and row[1] == hashed_password:
                    print(f"Logged in as '{username}'.")
                    return username
            else:
                print("Invalid data format in accounts file.")
                return None
    
    print("Invalid username or password.")
    return None

def delete_account():
    username = input("Enter username to delete account: ")
    
    lines = []
    deleted = False
    with open(ACCOUNTS_FILE, 'r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)
        lines.append(header)
        for line in reader:
            if line[0] == username:
                print(f"Deleted account: {line[0]}")
                deleted = True
            else:
                lines.append(line)
    
    if not deleted:
        print(f"Account '{username}' not found.")
    
    with open(ACCOUNTS_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(lines)

def view_all_account_info(username):
    print(f"All Info for Account '{username}':")
    with open(CSV_FILE, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['account_id'] == username:
                print(f"ID: {row['id']}, Partition: {row['partition_name']}, Chunk: {row['chunk_name']}, Voxel Index: {row['voxel_index']}, Data: {row['data']}")

def view_account_info(username):
    print(f"Account Info for '{username}':")
    with open(CSV_FILE, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['account_id'] == username:
                print(f"ID: {row['id']}, Partition: {row['partition_name']}, Chunk: {row['chunk_name']}, Voxel Index: {row['voxel_index']}, Data: {row['data']}")

def partition_exists(partition_name, account_id):
    with open(CSV_FILE, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if row[2] == partition_name and row[1] == account_id:
                return True
    return False

def chunk_exists(chunk_name, partition_name, account_id):
    with open(CSV_FILE, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if row[3] == chunk_name and row[2] == partition_name and row[1] == account_id:
                return True
    return False

def get_next_id():
    with open(CSV_FILE, 'r', newline='') as file:
        reader = csv.reader(file)
        data = list(reader)
        if len(data) <= 1:
            return '1'
        last_id = int(data[-1][0])
        return str(last_id + 1)

def add_partition(account_id):
    while True:
        partition_name = input("Enter the partition name: ")
        
        if partition_exists(partition_name, account_id):
            print(f"Partition '{partition_name}' already exists for this account.")
        else:
            with open(CSV_FILE, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([get_next_id(), account_id, partition_name, '', '', ''])
            print(f"Partition '{partition_name}' added successfully.")
            break

def remove_partition(account_id):
    partition_name = input("Enter the partition name to remove: ")
    
    lines = []
    found = False
    with open(CSV_FILE, 'r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)
        lines.append(header)
        for line in reader:
            if line[2] == partition_name and line[1] == account_id:
                print(f"Removed partition: {line[2]}")
                found = True
            else:
                lines.append(line)
    
    if not found:
        print(f"Partition '{partition_name}' not found or you don't have access.")
    
    with open(CSV_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(lines)

def add_chunk(account_id):
    while True:
        partition_name = input("Enter the partition name: ")
        
        if not partition_exists(partition_name, account_id):
            add_partition(account_id)
        
        chunk_name = input("Enter the chunk name: ")
        
        if chunk_exists(chunk_name, partition_name, account_id):
            print(f"Chunk '{chunk_name}' already exists in partition '{partition_name}'.")
        else:
            with open(CSV_FILE, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([get_next_id(), account_id, partition_name, chunk_name, '', ''])
            print(f"Chunk '{chunk_name}' added successfully.")
            break

def remove_chunk(account_id):
    partition_name = input("Enter the partition name: ")
    
    if not partition_exists(partition_name, account_id):
        print(f"Partition '{partition_name}' does not exist or you don't have access.")
        return
    
    chunk_name = input("Enter the chunk name to remove: ")
    
    lines = []
    found = False
    with open(CSV_FILE, 'r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)
        lines.append(header)
        for line in reader:
            if line[3] == chunk_name and line[2] == partition_name and line[1] == account_id:
                print(f"Removed chunk: {line[3]}")
                found = True
            else:
                lines.append(line)
    
    if not found:
        print(f"Chunk '{chunk_name}' not found or you don't have access.")
    
    with open(CSV_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(lines)

def add_voxel(account_id):
    while True:
        partition_name = input("Enter the partition name: ")
        
        if not partition_exists(partition_name, account_id):
            add_partition(account_id)
        
        chunk_name = input("Enter the chunk name: ")
        
        if not chunk_exists(chunk_name, partition_name, account_id):
            add_chunk(account_id, partition_name)
        
        voxel_dim = int(input("Enter the voxel dimension (e.g., 2 for a 2x2x2 voxel): "))
        
        while True:
            try:
                voxel_index = int(input(f"Enter the voxel index (0 to {voxel_dim ** 3 - 1}): "))
                if 0 <= voxel_index < voxel_dim ** 3:
                    break
                else:
                    print(f"Invalid voxel index. Please enter a number between 0 and {voxel_dim ** 3 - 1}.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        
        data = input(f"Enter data for voxel index {voxel_index}: ")
        
        lines = []
        found = False
        with open(CSV_FILE, 'r', newline='') as file:
            reader = csv.reader(file)
            header = next(reader)
            lines.append(header)
            for line in reader:
                if line[3] == chunk_name and line[2] == partition_name and line[1] == account_id:
                    if line[4] == '':
                        line[4] = [None] * (voxel_dim ** 3)
                        line[5] = [None] * (voxel_dim ** 3)
                    line[4][voxel_index] = voxel_index
                    line[5][voxel_index] = data
                    found = True
                lines.append(line)
        
        if not found:
            print(f"Chunk '{chunk_name}' not found or you don't have access.")
            continue
        
        with open(CSV_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(lines)
        
        print(f"Data '{data}' added to voxel index '{voxel_index}' in chunk '{chunk_name}'.")
        
        choice = input("Do you want to add more voxel data? (y/n): ").lower()
        if choice != 'y':
            break

def remove_voxel(account_id):
    while True:
        partition_name = input("Enter the partition name: ")
        
        if not partition_exists(partition_name, account_id):
            add_partition(account_id)
        
        chunk_name = input("Enter the chunk name: ")
        
        if not chunk_exists(chunk_name, partition_name, account_id):
            add_chunk(account_id)
        
        lines = []
        found = False
        with open(CSV_FILE, 'r', newline='') as file:
            reader = csv.reader(file)
            header = next(reader)
            lines.append(header)
            for line in reader:
                if line[3] == chunk_name and line[2] == partition_name and line[1] == account_id:
                    line[4] = ''
                    line[5] = ''
                    print(f"Removed voxel data from chunk '{chunk_name}'.")
                    found = True
                lines.append(line)
        
        if not found:
            print(f"Chunk '{chunk_name}' not found or you don't have access.")
            continue
        
        with open(CSV_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(lines)
        
        break

def main_menu():
    create_csv_if_not_exists()
    create_accounts_csv_if_not_exists()
    logged_in_user = None
    
    while True:
        if not logged_in_user:
            print("1. Create Account")
            print("2. Login")
            print("3. Quit")
            choice = input("Choose an option: ")
            
            if choice == '1':
                create_account()
            elif choice == '2':
                logged_in_user = login()
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        else:
            print(f"Logged in as '{logged_in_user}':")
            print("1. Add Partition")
            print("2. Add Chunk")
            print("3. Add Voxel Data")
            print("4. Remove Partition")
            print("5. Remove Chunk")
            print("6. Remove Voxel Data")
            print("7. View All My Info")
            print("8. View Account Info")
            print("9. Delete Account")
            print("10. Logout")
            choice = input("Choose an option: ")
            
            if choice == '1':
                add_partition(logged_in_user)
            elif choice == '2':
                add_chunk(logged_in_user)
            elif choice == '3':
                add_voxel(logged_in_user)
            elif choice == '4':
                remove_partition(logged_in_user)
            elif choice == '5':
                remove_chunk(logged_in_user)
            elif choice == '6':
                remove_voxel(logged_in_user)
            elif choice == '7':
                view_all_account_info(logged_in_user)
            elif choice == '8':
                view_account_info(logged_in_user)
            elif choice == '9':
                delete_account()
                logged_in_user = None
            elif choice == '10':
                print(f"Logged out from '{logged_in_user}'.")
                logged_in_user = None
            else:
                print("Invalid choice. Please enter a number from 1 to 10.")

if __name__ == "__main__":
    main_menu()
