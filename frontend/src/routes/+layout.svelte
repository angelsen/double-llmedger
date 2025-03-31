<script lang="ts">
	import '../app.css';
	import { ModeWatcher } from "mode-watcher";
	let { children } = $props();
</script>

<ModeWatcher />
<div class="min-h-screen bg-gradient-to-br from-background to-muted">
	{@render children()}
</div>
