<script>
	import { businessManagerStore } from './store.js';
    import Trader from './Trader.svelte';

	// Subscribe to the store and get the current value
	const businessManagerData = $businessManagerStore;

    const traders = businessManagerData.traders || [];

	function cloneAll() {
		// Handle clone all logic
		console.log('Clone All button clicked');
	}

	function publish() {
		// Handle publish logic
		businessManagerData.time_status = 'Published';
		console.log('Publish button clicked ${businessManagerData.time_status}');
	}

	function prepareEmail() {
		// Handle email preparation logic
	}
</script>

<main>
	<h1>
		{$businessManagerStore.name}
		<span
			class="status-box"
			class:statut-unfilled={businessManagerData.time_status === 'Unfilled'}
			class:statut-published={businessManagerData.time_status === 'Published'}
			>{businessManagerData.time_status}</span
		>
	</h1>
	<div class="button-container">
		<button class="button" on:click={cloneAll}>Clone All</button>
		<button class="button" on:click={publish}>Publish</button>
        <button class="button" on:click={publish}>Reminder</button>
		<button class="button" on:click={prepareEmail}>Help</button>
	</div>
	<div class="button-new-trader">
		<button on:click={cloneAll}>
			<i class="fas fa-plus"></i> Add Trader
		</button>
	</div>
    <div class="divider"></div>
    {#each traders as trader}
        <Trader trader={trader} />
    {/each}

    
</main>

<style>
	main {
		display: flex;
		flex-direction: column;
		align-items: flex-start; /* Align content to the left */
		padding: 20px;
	}

    .divider {
        width: 100%;
        height: 1px; /* Adjust the height as needed */
        background-color: #ccc; /* Adjust the color as needed */
        margin-bottom: 1px; /* Adjust the spacing between components */
        margin-top: 10px;
    }

	h1 {
		font-size: 24px;
		margin-bottom: 5px;
	}

	.status-box {
		width: 55px;
		padding: 2x;
		border: 2px solid #333;
		border-radius: 5px;
		text-align: center;
		font-weight: bold;
		margin-top: 10px;
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

	.button-container {
		margin-top: 4px;
		display: flex;
		gap: 10px;
	}

	.button {
		padding: 10px;
		background-color: #333;
		color: white;
		border: none;
		border-radius: 5px;
		cursor: pointer;
	}

	.button-new-trader {
		display: flex;
		align-items: center;
		justify-content: flex-start;
		margin-top: 20px;
	}

	.button-new-trader button {
		padding: 1px 3px;
		border: none;
		background-color: #4caf50;
		color: white;
		border-radius: 5px;
		cursor: pointer;
	}
</style>
