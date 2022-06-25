import os, shutil, zipfile

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join(path, '..')))


def percentage_calculation(perc_value, total_elm):
    value_p = int((int(perc_value) * int(total_elm)) / 100)

    return value_p


def copy_and_split_files(dir_path, dataset_split, train_dir, val_dir, test_dir, main_dir, path_report):

    file_list_dir = list()
    num_files = len([name for name in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, name))])

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
          f' - Training Directory (train: {train_value} files, val: {val_value} files)\n - Test Directory {test_value} files \n',
          file=open(path_report, 'a'))

    for file in os.listdir(dir_path):
        if file.endswith('.png'):
            file = os.path.join(dir_path, file)
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
              f'created at the following path {main_dir}, try another solution to improve performances. \n',
              file=open(path_report, 'a'))

    with zipfile.ZipFile(main_dir + '.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipdir(main_dir, zipf)


def dataset_creation(original_dir_path, main_dir_name, dataset_split, path_report):
    sub_folders = list()
    new_sub_folders = list()

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

        for sub_folder in os.walk(original_dir_path):
            path_folder = sub_folder[0].replace(APP_ROOT + '/', '')
            if not path_folder == original_dir_path:
                sub_folders.append(path_folder)

        if not sub_folders:
            copy_and_split_files(original_dir_path, dataset_split, train_dir, val_dir, test_dir, main_dir_name, path_report)
        else:

            for path in sub_folders:
                train_dir_sub = path.replace(original_dir_path, train_dir + '/')
                val_dir_sub = path.replace(original_dir_path, val_dir + '/')
                test_dir_sub = path.replace(original_dir_path, test_dir + '/')
                new_sub_folders.append(train_dir_sub)
                new_sub_folders.append(val_dir_sub)
                new_sub_folders.append(test_dir_sub)
                os.makedirs(train_dir_sub)
                os.makedirs(val_dir_sub)
                os.makedirs(test_dir_sub)
                print(f'File: {path}', file=open(path_report, 'a'))
                copy_and_split_files(path, dataset_split, train_dir_sub, val_dir_sub, test_dir_sub, main_dir_name, path_report)


if __name__ == '__main__':

    print(f'DATASET CREATION - Vigimella 2022 | Beta \nThis tool allows splitting out files to create a dataset.\nPlease in percentage dataset splitting insert only valid settings in specific format. (Example: 70-30, 80-20)\n')

    input_dataset = input(f'Insert percentage (training-test): ')
    input_directory = input(f'Insert path of directory where files are stored: ')
    dataset_name = input(f'Insert the name of dataset: ')
    report_name = input(f'Insert the name of report: ')

    check_one = input_dataset.split('-')[0]
    check_two = input_dataset.split('-')[1]

    if not '-' in input_dataset or not (int(check_one) + int(check_two) == 100):

        print('Not valid input, please retry!')
        exit(-1)

    else:

        path_report = os.path.join(APP_ROOT, report_name+'.txt')
        if os.path.isfile(path_report):
            os.remove(path_report)
        print(f'Dataset division: {input_dataset}', file=open(path_report, 'a'))
        dataset_creation(input_directory, dataset_name, input_dataset, path_report)
