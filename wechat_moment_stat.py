# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('UTF8')

import json

f = open('moments_output.json' ,'r')
json_raw = f.read()
f.close()

origin_data = json.loads(json_raw)
result = []

def get_user(user_name):
	for user_info in result:
		if user_info['user'] == user_name:
			return user_info
	user_info = {
		'user' : user_name,
		'moments' : [],
		'post_comments' : [],
		'replied_comments' : [],
		'received_comments' : [],
		'post_likes' : 0,
		'received_likes' : 0,
		'spam_counts' : 0,
	}
	result.append(user_info)
	return user_info

def is_spam(moment_text):
	if ('投' in moment_text and '谢' in moment_text):
		return True
	if ('投票' in moment_text):
		return True
	if ('问卷' in moment_text):
		return True
	if ('填' in moment_text and '谢' in moment_text):
		return True
	return False

def handle_moment(moment):
	user_info = get_user(moment['author'])
	user_info['moments'].append(moment)
	user_info['received_likes'] = user_info['received_likes'] + len(moment['likes'])
	user_info['received_comments'].extend(moment['comments'])
	if (is_spam(moment['content'])):
		user_info['spam_counts'] = user_info['spam_counts'] + 1
	for comment_info in moment['comments']:
		comment_user = get_user(comment_info['author'])
		comment_user['post_comments'].append(comment_info)
		if (comment_info['to_user'] != ''):
			replied_user = get_user(comment_info['to_user'])
			replied_user['replied_comments'].append(comment_info)
	for like_info in moment['likes']:
		like_user = get_user(like_info)
		like_user['post_likes'] = like_user['post_likes'] + 1

for moment_info in origin_data:
	handle_moment(moment_info)

f = open('user_output.json', 'w')
f.write(json.dumps(result))
f.close()

post_moment_rank = sorted(result, key=lambda user_info: len(user_info['moments']), reverse=True)
post_like_rank = sorted(result, key=lambda user_info: user_info['post_likes'], reverse=True)
received_like_rank = sorted(result, key=lambda user_info: user_info['received_likes'], reverse=True)
post_comment_rank = sorted(result, key=lambda user_info: len(user_info['post_comments']), reverse=True)
received_comment_rank = sorted(result, key=lambda user_info: len(user_info['received_comments']), reverse=True)
no_reply_rank = sorted(result, key=lambda user_info: ((float(len(user_info['replied_comments']))/len(user_info['post_comments'])) if len(user_info['post_comments'])>0 else 999))
spam_rank = sorted(result, key=lambda user_info: user_info['spam_counts'], reverse=True)

f = open('post_moment_rank.json', 'w')
f.write(json.dumps(post_moment_rank))
f.close()

print('前5位发最多朋友圈：')
temp_list = []
for i in range(5):
	temp_list.append(post_moment_rank[i]['user'] + '(%d 条)' % len(post_moment_rank[i]['moments']))
print(', '.join(temp_list))

f = open('post_like_rank.json', 'w')
f.write(json.dumps(post_like_rank))
f.close()

print('前5位点赞狂魔：')
temp_list = []
for i in range(5):
	temp_list.append(post_like_rank[i]['user'] + '(%d 赞)' % post_like_rank[i]['post_likes'])
print(', '.join(temp_list))

f = open('received_like_rank.json', 'w')
f.write(json.dumps(received_like_rank))
f.close()

print('前5位获得最多赞：')
temp_list = []
for i in range(5):
	temp_list.append(received_like_rank[i]['user'] + '(%d 赞)' % received_like_rank[i]['received_likes'])
print(', '.join(temp_list))

f = open('post_comment_rank.json', 'w')
f.write(json.dumps(post_comment_rank))
f.close()

print('前5位评论狂魔：')
temp_list = []
for i in range(5):
	temp_list.append(post_comment_rank[i]['user'] + '(%d 评论)' % len(post_comment_rank[i]['post_comments']))
print(', '.join(temp_list))

f = open('received_comment_rank.json', 'w')
f.write(json.dumps(received_comment_rank))
f.close()

print('前5位朋友圈评论最多：')
temp_list = []
for i in range(5):
	temp_list.append(received_comment_rank[i]['user'] + '(%d 评论)' % len(post_comment_rank[i]['received_comments']))
print(', '.join(temp_list))

f = open('no_reply_rank.json', 'w')
f.write(json.dumps(no_reply_rank))
f.close()

f = open('spam_rank.json', 'w')
f.write(json.dumps(spam_rank))
f.close()

print(' ')
print(' ')
print('==============你不用管下面的==================')
print(' ')
print(' ')

print('被华前5名（收到评论回复数／写评论数 且 发出评论数>=15）：')
temp_list = []
for user_info in no_reply_rank:
	if len(user_info['post_comments']) < 15:
		continue
	if (len(temp_list) > 5):
		break
	temp_list.append(user_info['user'] + ('(收到评论回复%d, 写评论%d)' % (len(user_info['replied_comments']), len(user_info['post_comments']))))
print(', '.join(temp_list))

