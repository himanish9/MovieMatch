export default function Header() {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-sm border-b border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="text-3xl">🎬</div>
          <div>
            <h1 className="text-xl font-bold text-foreground">MovieMatch</h1>
            <p className="text-xs text-muted-foreground">Personalized Recommendations</p>
          </div>
        </div>
        <div className="hidden sm:block text-sm text-muted-foreground">
          AI-Powered Cinema Experience
        </div>
      </div>
    </header>
  );
}
