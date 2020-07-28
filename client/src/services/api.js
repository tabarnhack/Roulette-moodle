const login = async user => {
	return fetch(`${process.env.VUE_APP_ROOT_API}/login`, {
		method: "post", 
		credentials: "include",
		headers: {
			"Content-Type": "application/json",
			"Cache": "no-cache"
		},
		body: JSON.stringify({
			username: user.username,
			password: user.password,
		})
	}).then(res => {
		if(res.ok)
			return res.json()
		else
			return Promise.reject("Something went wrong")
	});
}

const check = async () => {
	return fetch(`${process.env.VUE_APP_ROOT_API}/check`, {credentials: "include"}).then(res => {
		if(res.ok || res.status === 400 || res.status === 401)
			return res.json()
		else
			return Promise.reject("Something went wrong")
	})
}

const courses = async () => {
	return fetch(`${process.env.VUE_APP_ROOT_API}/courses`, {credentials: "include"}).then(res => {
		if(res.ok || res.status === 400 || res.status === 401)
			return res.json()
		else
			return Promise.reject('Something went wrong')
	})
}

const grades = async (choice) => {
	return fetch(`${process.env.VUE_APP_ROOT_API}/grades?id=${choice}`, {credentials: "include"}).then(res => {
		if(res.ok || res.status === 400 || res.status === 401)
			return res.json()
		else
			return Promise.reject('Something went wrong')
	})
}

export { login, courses, grades, check }
