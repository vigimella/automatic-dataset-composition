import os, shutil

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def percentage_calculation(perc_value, total_elm):
    value_p = int((int(perc_value) * int(total_elm)) / 100)

    return value_p


def dataset_creation(original_dir_path, main_dir_name, dataset_split):

    file_list_dir = list()

    # defining paths to directories creation and creation of them

    main_dir = os.path.join(APP_ROOT, main_dir_name)

    # Check if dataset already exists

    if os.path.exists(main_dir):
        print(f'Dataset with name: "{main_dir_name}" already exists. It will be deleted and re-created.')
        shutil.rmtree(main_dir)
    else:
        os.makedirs(main_dir)

    training_dir = os.path.join(main_dir_name, 'training')
    os.makedirs(training_dir)
    test_dir = os.path.join(main_dir_name, 'test')
    os.makedirs(test_dir)
    train_dir = os.path.join(training_dir, 'train')
    os.makedirs(train_dir)
    val_dir = os.path.join(training_dir, 'val')
    os.makedirs(val_dir)

    # calculating num of elements stored in main folder

    if not os.path.exists(original_dir_path):

        print(f'No such directory "{original_dir_path}"')

    else:

        num_files = len(
            [name for name in os.listdir(original_dir_path) if os.path.isfile(os.path.join(original_dir_path, name))])

        # calculating of elements to store in training dir
        training_value = dataset_split.split('-')[0]
        training_value = percentage_calculation(training_value, num_files)

        # calculating of elements to store in test dir
        test_value = dataset_split.split('-')[1]
        test_value = percentage_calculation(test_value, num_files)

        num_files_training = num_files - test_value

        # calculating of elements to store in train dir
        train_value = dataset_split.split('-')[0]
        train_value = percentage_calculation(train_value, num_files_training)
        # calculating of elements to store in val dir
        val_value = dataset_split.split('-')[1]
        val_value = percentage_calculation(val_value, num_files_training)

        print(f'Directory contains {num_files} files. Dataset will be divided in:\n'
              f' - Training Directory (train: {train_value} files, val: {val_value} files)\n - Test Directory {test_value} files')

        for file in os.listdir(original_dir_path):
            if file.endswith('.png'):
                file = os.path.join(original_dir_path, file)
                file_list_dir.append(file)

        for file in file_list_dir[:train_value]:
            shutil.copy(file, train_dir)
            file_list_dir.remove(file)

        for file in file_list_dir[:val_value]:
            shutil.copy(file, val_dir)
            file_list_dir.remove(file)

        for file in file_list_dir[:test_value]:
            shutil.copy(file, test_dir)
            file_list_dir.remove(file)

        if file_list_dir.__len__() > 0:
            print(f'{file_list_dir.__len__()} file(s) cannot be included inside the dataset.\nAnyway your dataset has '
                  f'created at the following path {main_dir}, try another solution to improve performances.')


if __name__ == '__main__':

    print(f'DATASET CREATION - Vigimella 2022 | Beta \nThis tool allows splitting out files to create a dataset.\nPlease in percentage dataset splitting insert only valid settings in specific format. (Example: 70-30, 80-20)\n')

    input_dataset = input(f'Insert percentage (training-test): ')
    input_directory = input(f'Insert path of directory where files are stored: ')
    dataset_name = input(f'Insert the name of dataset: ')

    check_one = input_dataset.split('-')[0]
    check_two = input_dataset.split('-')[1]

    if not '-' in input_dataset or not (int(check_one) + int(check_two) == 100):

        print('Not valid input, please retry!')
        exit(-1)

    else:

        dataset_creation(input_directory, dataset_name, input_dataset)
        #dataset_creation('/home/vigimella/Desktop/attempt_dataset/', 'prova', input_dataset)

