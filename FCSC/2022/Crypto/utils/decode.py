import random

def shuffle_under_seed(ls, seed):
  # Shuffle the list ls using the seed `seed`
  random.seed(seed)
  random.shuffle(ls)
  return ls

def unshuffle_list(shuffled_ls, seed):
  n = len(shuffled_ls)
  # Perm is [1, 2, ..., n]
  perm = [i for i in range(1, n + 1)]
  # Apply sigma to perm
  shuffled_perm = shuffle_under_seed(perm, seed)
  # Zip and unshuffle
  zipped_ls = list(zip(shuffled_ls, shuffled_perm))
  zipped_ls.sort(key=lambda x: x[1])
  return [a for (a, b) in zipped_ls]

def Convert(string):
    list1=[]
    list1[:0]=string
    return list1

shuffled_str = "f668cf029d2dc4234394e3f7a8S9f15f626Cc257Ce64}2dcd93323933d2{F1a1cd29db"
shuffled_ls = Convert(shuffled_str)
print("Shuffled string : ", shuffled_str)

for i in range(256):
    unshuffled_ls = unshuffle_list(shuffled_ls, i)
    unshuffled_string = "".join(unshuffled_ls)
    print(unshuffled_string)
