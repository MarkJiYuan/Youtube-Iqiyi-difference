'引入模块'
import time
import json
import re
import os
import jieba

'全局变量'

'类'
class Timer:
    start = time.time()
    init_start = start

    def time_past(self):
        end = time.time()
        print('************************************')
        print('程序用时:%f' % (end - self.start))
        print('************************************')
        self.start = time.time()

    def time_past_all(self):
        end = time.time()
        print('************************************')
        print('程序用时:%f' % (end - self.init_start))
        print('************************************')

'函数'

def show_tags(s):
	i = re.findall(r'<[a-zA-Z]+\s|<[a-zA-Z]+>',s)
	dict = {}
	for a in i:
		c = a.replace("<","").replace(">","").replace(" ","")
		if not c in dict:
			dict[c] = 1
		else:
			dict[c] += 1
	return dict

def show_texts(s):
	l = re.findall(r'>(.*?)<', s)
	l = [ text.replace(" ", "") for text in l ]
	l = [ text for text in l if text != "" ]
	return l

def is_video(s):
	for i in range(len(s)):
		if s[i:i+5] == '<head':
			if s[i:i+14] == '<head itemprop':
				return True
			else:
				return False
	return False

def how_many_char(l):
	count = 0
	for chip in l:
		count += len(chip)
	return count

def get_video_length_iqiyi(s):
	video_length = ""
	for i in range(len(s)):
		if s[i:i+12] == '"duration":"':
			i = i + 12
			while s[i] != '"':
				video_length += s[i]
				i += 1
			return video_length
	return video_length

def get_video_length_youtube(s):
	video_length = ""
	for i in range(len(s)):
		if s[i:i+10] == 'Duration: ':
			i = i + 10
			while s[i] != '.':
				video_length += s[i]
				i += 1
			return video_length
	return video_length

def statistics(s):
	tags_l = show_tags(s)
	texts_l = show_texts(s)
	if is_video(s):
		video_length = get_video_length_iqiyi(s)
	else:
		video_length = ""
	char_num = how_many_char(texts_l)
	this_html_data = [tags_l, video_length, char_num]
	return this_html_data

def is_chinese(ch):
    if ch <  '一' or ch > '龥':
        return False
    return True

def valid_dict(d):
	new_d = d.copy()
	for word in new_d:
		if not is_chinese(word) or len(word) == 1:
			d.pop(word)
	return 

def valid_dict_english(d):
	new_d = d.copy()
	for word in new_d:
		if len(word) > 25:
			d.pop(word)
	return d



def save_more_urls(f_jl, d):
	with open(f_jl, 'r') as f:
		print('打开%s成功!' % f_jl)
		for line in f.readlines():
			try:
				this_url = json.loads(line)['url'][0]
				print(this_url, '打开成功！')
				urls = json.loads(line)['more_urls']

				# 处理下url，否则无法保存为txt。掐头去尾，换/为-
				this_url = this_url[8:-1].replace('/','-')

				with open(d + '/' + this_url + '.txt', 'w') as f:
					for u in urls:
						f.write(u + "\n")
			except:
				print('该网页读取失败！')
	print('全部文件已经保存在%s文件夹' % d)

def save_htmls(f_jl, d):
	with open(f_jl, 'r') as f:
		print('打开%s成功!' % f_jl)
		for line in f.readlines():
			try:
				this_url = json.loads(line)['url'][0]
				html_body = json.loads(line)['html_body'][0]

				this_url = this_url.strip()
				this_url = this_url[8:].replace('/','-')

				with open(d + '/' + this_url + '.html', 'w') as f:
					f.write(html_body)
				print('%s已成功保存' % this_url)
			except:
				print('该网页读取失败！')
	print('全部文件已经保存在%s文件夹' % d)


def time_to_seconds(s):
	seconds = 0
	l = list(map(int, s.split(':')))
	if len(l) == 3:
		seconds = 3600 * l[0] + 60 * l[1] + l[2]
	else:
		seconds = 60 * l[0] + l[1]
	return seconds

'主函数'
def main(*args, **kw):

	'爱奇艺统计'
	# data = {"tags":[], "video_length":[], "valid_char_num":[]}
	# words = {}

	# count = 0
	# os.chdir('iqiyi_htmls')
	# file_list = os.listdir()
	# print(len(file_list))
	# for file in file_list:
	# 	with open(file, 'r') as f:
	# 		try:
	# 			s = f.read()
	# 			one_data = statistics(s)
	# 			data["tags"].append(one_data[0])
	# 			data["video_length"].append(one_data[1])
	# 			data["valid_char_num"].append(one_data[2])
	# 			count += 1
	# 			print('处理进度：', int(count / 1034 * 100), '%')
	# 			for word in jieba.lcut("".join(show_texts(s))):
	# 				if word in words:
	# 					words[word] += 1
	# 				else:
	# 					words[word] = 1
	# 		except:
	# 			print(file, '统计失败')
	# data['video_length'] = [ length for length in data['video_length'] if length != '']
	# print(data)
	# words = valid_dict(words)
	# words = sorted(words.items(), key=lambda d:d[1], reverse=False)
	# print(words)

	# with open('iqiyi_data.txt', 'w', encoding='utf-8') as f:
	# 	f.write(json.dumps(data))
	# with open('iqiyi_word.txt', 'w', encoding='utf-8') as f:
	# 	f.write(json.dumps(words))


	'Youtube统计'
	data = {"tags":[], "video_length":[], "valid_char_num":[]}
	words = {}

	count = 0
	os.chdir('youtube_htmls')
	file_list = os.listdir()
	print(len(file_list))
	for file in file_list:
		with open(file, 'r') as f:
			try:
				s = f.read()
				data['tags'].append(show_tags(s))
				if 'watch' in file:
					data['video_length'].append(get_video_length_youtube(s))
				data['valid_char_num'].append(how_many_char(show_texts(s)))

				count += 1
				print('处理进度：', int(count / 1793 * 100), '%')
				for word in " ".join(show_texts(s)).split():
					if word in words:
						words[word] += 1
					else:
						words[word] = 1
			except:
				print(file, '统计失败')
	data['video_length'] = [ length for length in data['video_length'] if length != '']
	print(data)
	words = valid_dict_english(words)
	words = sorted(words.items(), key=lambda d:d[1], reverse=False)
	print(words)
	os.chdir('..')


	with open('youtube_data.txt', 'w', encoding='utf-8') as f:
		f.write(json.dumps(data))
	with open('yourube_word.txt', 'w', encoding='utf-8') as f:
		f.write(json.dumps(words))



'直接运行该模块'
if __name__ == '__main__':
    clock = Timer()
    main()
    clock.time_past_all()



