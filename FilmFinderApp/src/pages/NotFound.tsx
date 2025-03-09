export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100 text-gray-800">
      <h1 className="text-6xl font-bold mb-4">404</h1>
      <h2 className="text-2xl font-semibold mb-2">Page Not Found</h2>
      <p className="text-lg mb-6">The page you're looking for doesn't exist.</p>
      <a
        href="/"
        className="px-6 py-3 bg-blue-500 text-white rounded-lg text-lg hover:bg-blue-600 transition"
      >
        Go Home
      </a>
    </div>
  );
}
