<script>
	//import { businessManagerStore } from './store.js';
	import TraderTimes from './TraderTimes.svelte';

	// Subscribe to the store and get the current value
	//const businessManagerData = $businessManagerStore;

	export let trader;

	function Reminder() {
		// Handle publish logic
		console.log('Reminder button clicked');
	}
</script>

<main>
	<div class="container-trader">
		<h2>
			{trader.name}<span
				class="status-box"
				class:statut-unfilled={trader.status === 'Unfilled'}
				class:statut-published={trader.status === 'Published'}>{trader.status}</span
			>
		</h2>
		<h4>Entity: {trader.entity}</h4>
		<h5>Product Line: {trader.product_line}</h5>
	</div>
	<div class="container-trader-times">
		<TraderTimes cdrs={trader.cdrs} />
	</div>
	<div class="button-new-cdr">
		<button on:click={Reminder}>
			<i class="fas fa-plus"></i> Add Cdr
		</button>
	</div>
</main>

<style>
	main {
		display: flex;
		flex-direction: column;
		align-items: flex-start; /* Align content to the left */
		padding: 0px;
	}

	h2 {
		font-size: 24px;
		margin-bottom: 5px;
	}

	.status-box {
		width: 45px;
		padding: 2x;
		border: 2px solid #333;
		border-radius: 5px;
		text-align: center;
		font-weight: bold;
		margin-top: 10px;
		margin-left: 2px;
		margin-right: 5px;
		font-size: 12px;
		display: inline-block; /* Pour s'assurer que la boîte de statut ne prend pas toute la largeur */
	}

	.statut-unfilled {
		background-color: #ff6666; /* Light red */
		color: white;
	}

	.statut-published {
		background-color: #90ee90; /* Light red */
		color: white;
	}

	h4 {
		margin-bottom: 2px;
	}

	h5 {
		margin-top: 2px;
		margin-bottom: 2px;
	}

	p {
		margin-bottom: 1px;
	}

	.button-container {
		margin-top: 4px;
		display: flex;
		gap: 10px;
	}

	.button {
		padding: 4px;
		background-color: #333;
		color: white;
		border: none;
		border-radius: 5px;
		cursor: pointer;
	}

	.button-new-cdr {
		display: flex;
		align-items: center;
		justify-content: flex-start;
		margin-top: 15px;
	}

	.button-new-cdr button {
		padding: 0.2px 1.5px;
		border: none;
		background-color: #4caf50;
		color: white;
		border-radius: 5px;
		cursor: pointer;
	}
</style>
