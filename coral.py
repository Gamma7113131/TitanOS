import requests
import json

def load_session(usr):
	with open("coral_sessions.json", 'r') as file:
		sessions = json.load(file)
		return sessions.get(usr, False)

def save_session(usr, session):
	with open("coral_sessions.json", 'r') as file:
		sessions = json.load(file)
	sessions[usr] = session
	with open("coral_sessions.json", 'w') as file:
		json.dump(sessions, file, indent=4)

def talk_to_coral(user, query):
	session = load_session(user)
	if not session:
		session = {
			"model":"Qwen/Qwen2.5-72B-Instruct",
        	"messages":[{"role":"system","content":"You are Coral, an AI assistant integrated into TitanOS. Your goal is to assist the user in the most efficient way possible, depending on their requests. To do this, you have access to system commands. Here they are: '!mkfile <path/to/file'>' using this command you can create files for a user. The default filesystem starts at '/' which is the user's home directory. Next command: '!mkdir <path/to/dir>' using this command you can make folders within the '/' directory. To use these commands, put them somewhere within your response. You can use multiple commands in a response."}],
        	"temperature":0.5,
        	"max_tokens":2048,
        	"top_p":0.7
    	}
	session["messages"].append({"role":"user","content":query})

	response = requests.post("https://api-inference.huggingface.co/models/Qwen/Qwen2.5-72B-Instruct/v1/chat/completions", headers={
		"accept": "*/*",
    	"accept-encoding": "gzip, deflate, br, zstd",
    	"accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    	"authorization": "Bearer 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",
    	"content-length": "239",
    	"content-type": "application/json",
    	"origin": "https://huggingface-inference-playground.hf.space",
    	"priority": "u=1, i",
    	"referer": "https://huggingface-inference-playground.hf.space/",
    	"sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Opera GX";v="114"',
    	"sec-ch-ua-mobile": "?0",
    	"sec-ch-ua-platform": '"Windows"',
    	"sec-fetch-dest": "empty",
    	"sec-fetch-mode": "cors",
    	"sec-fetch-site": "cross-site",
    	"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0",
    	"x-use-cache": "false"
	}, json=session)

	if not "choices" in response.json():
		return response.json()
	to_return = response.json()['choices'][0]['message']['content']
	session['messages'].append({'role':'assistant', 'content':to_return})
	save_session(user, session)
	return to_return
	
