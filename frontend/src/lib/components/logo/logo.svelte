<script lang="ts">
  export let size: 'sm' | 'md' | 'lg' = 'md';
  export let variant: 'default' | 'dashboard' = 'default';
  
  // Dynamically set the class based on size
  const sizeClasses = {
    sm: 'text-xl',
    md: 'text-2xl',
    lg: 'text-3xl',
  };
  
  const sizeClass = sizeClasses[size];
</script>

<div class="{sizeClass} font-extrabold tracking-tighter select-none {$$props.class || ''}">
  <span class="logo-container">
    <span class="text-primary">double</span>
    <span class="ll-highlight">LL</span>
    <span class="text-primary">Medger</span>
    {#if variant === 'dashboard'}
      <span class="text-xs font-semibold tracking-wide align-top ml-1 bg-primary text-primary-foreground px-1.5 py-0.5 rounded-md">
        alpha
      </span>
    {/if}
  </span>
</div>

<style>
  .logo-container {
    position: relative;
    display: inline-flex;
    align-items: center;
  }
  
  .ll-highlight {
    position: relative;
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
    background-clip: text;
    -webkit-background-clip: text;
    color: transparent;
    font-style: italic;
    font-weight: 900;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    transform: skew(-8deg);
    display: inline-block;
    letter-spacing: -1px;
  }
  
  .ll-highlight::after {
    content: '';
    position: absolute;
    bottom: 2px;
    left: 0;
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%);
    border-radius: 1px;
  }
</style>