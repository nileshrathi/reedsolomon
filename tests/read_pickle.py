import pickle 
msg_len_file=open('msg_len_arr.obj', 'r')
nsym_len_file=open('nsym_len_arr.obj', 'r')
enc_time_file=open('enc_time_arr.obj', 'r')
dec_time_file=open('dec_time_arr.obj', 'r')
msg_len_array=pickle.load(msg_len_file)
nsym_len_array=pickle.load(nsym_len_file)
enc_time_array=pickle.load(enc_time_file)
dec_time_array=pickle.load(dec_time_file)

print(msg_len_array)
print(nsym_len_array)
print(enc_time_array)
print(dec_time_array)