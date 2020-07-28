<template>
	<div class="about">
		<div class="info small-container">
			<h1>A propos</h1>
			<img src="../assets/profile.png"/>
			<p>
				Réalisé avec 
				<font-awesome-icon icon="heart" />
				et un beaucoup de 
				<font-awesome-icon icon="coffee" />
				par <a href="https://github.com/tabarnhack" target="_blank" rel="noopener">Tabarnhack</a>.
			</p>
			<p>Application distribuée sous <a href="https://github.com/tabarnhack/Roulette-moodle/blob/master/LICENSE">licence GPL-3.0</a></p>
		</div>
	</div>
</template>

<script>
export default {
	name: 'About'
}
</script>

<style scoped>
img {
	width: 15%;
	min-width: 270px;
}
</style>