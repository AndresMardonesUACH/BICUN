import "./globals.css";
import { Open_Sans } from 'next/font/google'
import { Provider } from "@/components/ui/provider"

//👇 Configure our font object
const openSans = Open_Sans({
  subsets: ['latin'],
  display: 'swap',
})

export const metadata = {
  title: "BICUN",
  description: "Biblioteca Comunitaria Universitaria",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={openSans.className} suppressHydrationWarning>
      <body>
        <Provider>
          {children}
        </Provider>
      </body>
    </html>
  );
}
