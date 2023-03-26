import json
import jsonlines
import random

def filter_objects_by_text(arr1, arr2):
    text_set2 = set(obj2["text"] for obj2 in arr2)
    text_set1 = set(obj1["text"] for obj1 in arr1)

    text_filter = text_set1 & text_set2

    unique_texts1 = set()
    arr1_filtered = []
    for obj1 in arr1:
        if obj1["text"] not in unique_texts1 and obj1["text"] in text_filter:
            arr1_filtered.append(obj1)
            unique_texts1.add(obj1["text"])
    return arr1_filtered

def count_labels(datasets, labels):
    count = {label: 0 for label in labels}
    label_counts = {label: label for label in labels}
    for dataset in datasets:
        if "spans" in dataset:
            for span in dataset["spans"]:
                label = span.get("label")
                if label in count.keys():
                    count[label_counts[label]] += 1
    return count

def delete_objects_with_label(input_array, desired_delete_numbers, label_to_delete):
    # Use a list comprehension to filter the objects with the specified label
    # Find all elements with the specified label
    matching_elements = [element for element in input_array if element["accept"][0] == label_to_delete]
    
    # Determine how many elements to delete
    delete_count = min(len(matching_elements), desired_delete_numbers)
    
    # Delete random elements from the list
    deleted_elements = random.sample(matching_elements, delete_count)
    new_array = [element for element in input_array if element not in deleted_elements]
    
    # Return the new array and the deleted elements
    return (new_array, deleted_elements)

def save_to_jsonl(datasets, filepath):
    with open(f'{filepath}', 'w') as f1:
        for obj in datasets:
            json_str = json.dumps(obj)
            f1.write(json_str + '\n')


filepath = "./assets/prodigy"


dataset1 = []
dataset2 = []
# Load the two datasets
with jsonlines.open(f'{filepath}/annotator-1/final.jsonl', 'r') as f1, jsonlines.open(f'{filepath}/annotator-2/final.jsonl', 'r') as f2:


    for data in f1:
        if(len(data['accept'])>0):
            dataset1.append(data)

    for data in f2:
        if(len(data['accept'])>0):
            dataset2.append(data)

# Make dataset equal
dataset1_normalize = filter_objects_by_text(dataset1, dataset2)
dataset2_normalize = filter_objects_by_text(dataset2, dataset1)


# Balanced the dataset
dataset1_balanced, filter_delete = delete_objects_with_label(dataset1_normalize, 1000, "POSTCONDITION")
delete_ids = [obj["text"] for obj in filter_delete]
dataset2_balanced = [obj for obj in dataset2_normalize if obj["text"] not in delete_ids]

