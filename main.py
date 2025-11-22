import pickle

with open('feedback-raw-no-feedback-contents/courses.p', 'rb') as f:
    data = pickle.load(f)


print(type(data))
print(len(data))