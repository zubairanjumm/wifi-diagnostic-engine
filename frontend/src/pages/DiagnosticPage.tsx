interface DiagnosticPageProps {
  error: string | null
  onRetry: () => void
}

export function DiagnosticPage({
  error,
  onRetry,
}: DiagnosticPageProps) {
  return (
    <main className="mx-auto flex min-h-[75vh] max-w-3xl items-center justify-center px-6">
      <div className="w-full text-center">
        {error ? (
          <>
            <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full border border-black/10">
              !
            </div>

            <h1 className="mt-8 text-3xl font-semibold tracking-tight">
              We couldn't complete the diagnostic.
            </h1>

            <p className="mx-auto mt-4 max-w-md text-black/50">
              Make sure the diagnostic service is running
              and try again.
            </p>

            <button
              onClick={onRetry}
              className="mt-8 rounded-full bg-black px-6 py-3 text-sm font-medium text-white"
            >
              Try again
            </button>
          </>
        ) : (
          <>
            <div className="mx-auto h-14 w-14 animate-pulse rounded-full border border-black/20" />

            <h1 className="mt-8 text-3xl font-semibold tracking-tight">
              Checking your connection
            </h1>

            <p className="mt-4 text-black/50">
              Collecting network evidence from your browser...
            </p>

            <div className="mx-auto mt-10 h-1 max-w-xs overflow-hidden rounded-full bg-black/10">
              <div className="h-full w-1/2 animate-pulse rounded-full bg-black" />
            </div>
          </>
        )}
      </div>
    </main>
  )
}