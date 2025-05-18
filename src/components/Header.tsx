import { BellIcon, QuestionMarkCircleIcon } from '@heroicons/react/24/outline'

export default function Header() {
  return (
    <header className="bg-white shadow-sm">
      <div className="mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 justify-between items-center">
          <div className="flex items-center">
            <h1 className="text-2xl font-bold text-primary-600">WorkSight AI</h1>
            <p className="ml-3 text-sm text-gray-500">Intelligent HR Analytics & Predictions</p>
          </div>
          
          <div className="flex items-center space-x-4">
            <button className="p-2 text-gray-400 hover:text-gray-500">
              <BellIcon className="h-6 w-6" />
            </button>
            <button className="p-2 text-gray-400 hover:text-gray-500">
              <QuestionMarkCircleIcon className="h-6 w-6" />
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}