<template>
	<div class="home">
		<img alt="Moodle logo" src="../assets/logo.png">
		<div class="hello">
			<h1>Roulette Moodle</h1>
			<p>
				Une petite application afin de garder un certain suspense<br /> 
				lors de la transmission de notes à travers une plateforme 
				<a href="https://moodle.org" target="_blank" rel="noopener">Moodle</a>.
			</p>
			<p>Tout se passe par <router-link to="/wheel">ici</router-link>.</p>
			<h3>Pour plus d'infos</h3>
			<ul>
				<li><router-link to="/about">A propos</router-link></li>
			</ul>
		</div>
	</div>
</template>

<script>
export default {
	name: 'Home'
}
</script>

<style scoped>
img {
	width: 20%;
	min-width: 270px;
}
h3 {
	margin: 40px 0 0;
}
ul {
	list-style-type: none;
	padding: 0;
}
li {
	display: inline-block;
	margin: 0 10px;
}
a {
	color: #42b983;
}
</style>
