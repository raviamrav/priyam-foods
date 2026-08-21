<script setup lang="ts">
import { ref, onMounted } from "vue";
import { Analytics } from '@vercel/analytics/vue';

const firstName = ref("");
const lastName = ref("");
const whatsapp = ref("");
const email = ref("");
const address = ref("");
const contactPlatform = ref("whatsapp");

interface Item {
  name: string;
  price: number;
  quantity: number;
}

interface MenuCategory {
  category: string;
  items: Item[];
}

const menu = ref<MenuCategory[]>([]);
const isLoading = ref(true);

onMounted(async () => {
  isLoading.value = true;

  try {
    // const response = await fetch(`${import.meta.env.VITE_API_URL}/menu`)
    const response = await fetch(`${(window as any).APP_CONFIG.API_URL}/menu`);
    const menuData = await response.json();

    menu.value = menuData.map((category: any) => ({
      category: category.category,
      items: category.items.map((item: any) => ({
        name: item.name,
        price: Number(item.price),
        quantity: 0,
      })),
    }));
  } catch (error) {
    console.error("Error fetching menu:", error);
    // alert("Failed to load menu. Please try again later.");
    alert("⚠️ Service temporarily unavailable — monthly hosting limit reached.\nFor a live demo, please contact: raviamrav@yahoo.com");
  } finally {
    isLoading.value = false;
  }
});

async function storeVCF() {
  const vcfContent = `BEGIN:VCARD
VERSION:3.0
FN:Priyam Foods
TEL;TYPE=CELL:+4915207287460
EMAIL:priyam_foods@gmail.com
END:VCARD`;
  const blob = new Blob([vcfContent], { type: "text/vcard" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `PriyamFoods.vcf`;
  a.click();
}

async function submitOrder() {
  const selectedItems = menu.value
    .flatMap((category) => category.items)
    .filter((item) => item.quantity > 0);

  if (selectedItems.length === 0) {
    alert("Please select at least one item to order.");
    return;
  }

  const orderItems = selectedItems.map((item) => ({
    name: item.name,
    quantity: item.quantity,
  }));

  if (!whatsapp.value) {
    alert(`Error: Please enter your ${contactPlatform.value} number.`);
    return;
  }
  const customer = {
    first_name: firstName.value,
    last_name: lastName.value,
    whatsapp_number: whatsapp.value,
    address: address.value,
    email: email.value,
    contact_platform: contactPlatform.value,
  };

  const order = {
    customer: customer,
    items: orderItems,
  };
  //alert(JSON.stringify(order));
  console.log(JSON.stringify(order));

  const response = await fetch(`${(window as any).APP_CONFIG.API_URL}/order`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(order),
  });

  const data = await response.json();
  await navigator.clipboard.writeText(data.message)

  if (data.desktop_contact_link || data.mobile_contact_link || data.whatsapp_link) {
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    let linkToOpen = data.whatsapp_link; // fallback
    
    if (isMobile && data.mobile_contact_link) {
      linkToOpen = data.mobile_contact_link;
    } else if (!isMobile && data.desktop_contact_link) {
      linkToOpen = data.desktop_contact_link;
    } else if (data.contact_link) {
      linkToOpen = data.contact_link;
    }
    
    const platformName = contactPlatform.value === 'telegram' ? 'Telegram' : 'WhatsApp';
    alert("Order copied to clipboard.\n\n" +`Opening ${platformName} to place your order. If it doesn't open, please paste the message manually in your ${platformName} chat with us.`);
    window.open(linkToOpen, "_blank");

  } else {
    alert(`Couldn't open ${contactPlatform.value}`);
  }

  console.log(data);
}
</script>

<template>
  <div class="min-h-screen bg-orange-50 pb-20 font-sans">
    <!-- Hero Header -->
    <header class="bg-blue-800 shadow-sm py-10 mb-8 border-b-4 border-orange-500">
      <h1 class="text-5xl md:text-7xl font-black text-green-600 text-center uppercase tracking-tighter">
        Priyam Foods
      </h1>
      <p class="text-center text-white mt-2 italic">
        South Indian Moms Special | Authentic Tastes & Flavors | 100% Homemade | Fresh
        Ingredients | Order Now!
      </p>
    </header>

    <div class="max-w-4xl mx-auto px-4">
      <!-- Menu Sections -->
      
      <div v-if="isLoading" class="flex flex-col items-center justify-center py-20">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-t-4 border-b-4 border-orange-500 mb-4"></div>
        <p class="text-xl font-semibold text-gray-600">Loading menu...</p>
      </div>
      <div v-else>
        <div v-for="category in menu" :key="category.category" class="mb-10">
          <h2
            class="text-2xl font-bold text-gray-800 mb-4 border-l-4 border-orange-500 pl-3"
          >
            {{ category.category }}
          </h2>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div
              v-for="item in category.items"
              :key="item.name"
              :class="[
                'p-4 rounded-2xl border-2 transition-all duration-300 flex justify-between items-center bg-white shadow-sm',
                item.quantity > 0
                  ? 'border-green-500 bg-green-50'
                  : 'border-transparent hover:border-orange-200',
              ]"
            >
              <div>
                <h3 class="font-bold text-lg text-gray-800">{{ item.name }}</h3>
                <p class="text-orange-600 font-semibold">
                  €{{ item.price.toFixed(2) }}
                </p>
              </div>

              <div class="flex items-center gap-3 bg-gray-100 rounded-full p-1">
                <button
                  @click="item.quantity = Math.max(0, item.quantity - 1)"
                  class="w-8 h-8 rounded-full bg-white shadow flex items-center justify-center hover:bg-orange-500 hover:text-white transition"
                >
                  -
                </button>
                <span class="w-6 text-center font-bold">{{ item.quantity }}</span>
                <button
                  @click="item.quantity++"
                  class="w-8 h-8 rounded-full bg-white shadow flex items-center justify-center hover:bg-green-500 hover:text-white transition"
                >
                  +
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Checkout Form -->
      <div
        class="bg-white rounded-3xl shadow-xl p-8 mt-12 border border-gray-100"
      >
        <h2 class="text-3xl font-bold text-gray-800 mb-6 text-center">
          Delivery Details
        </h2>
        <div class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <input
              v-model="firstName"
              placeholder="First Name"
              class="w-full p-4 rounded-xl border-gray-200 border focus:ring-2 focus:ring-orange-500 outline-none"
            />
            <input
              v-model="lastName"
              placeholder="Last Name"
              class="w-full p-4 rounded-xl border-gray-200 border focus:ring-2 focus:ring-orange-500 outline-none"
            />
          </div>

          <div class="flex items-center gap-6 mb-2 mt-4 px-2">
            <label class="flex items-center gap-2 cursor-pointer">
              <input type="radio" value="whatsapp" v-model="contactPlatform" class="w-5 h-5 text-green-500 focus:ring-green-500" />
              <span class="font-medium text-gray-700">WhatsApp</span>
            </label>
            <label class="flex items-center gap-2 cursor-pointer">
              <input type="radio" value="telegram" v-model="contactPlatform" class="w-5 h-5 text-blue-500 focus:ring-blue-500" />
              <span class="font-medium text-gray-700">Telegram</span>
            </label>
          </div>

          <div class="flex items-center gap-2">
            <input
              v-model="whatsapp"
              type="tel"
              :placeholder="contactPlatform === 'whatsapp' ? 'WhatsApp Number' : 'Telegram Number'"
              class="flex-1 min-w-0 p-4 rounded-xl border-gray-200 border focus:ring-2 focus:ring-orange-500 outline-none"
            />
            <div
              v-if="contactPlatform === 'whatsapp'"
              class="bg-green-100 rounded-xl cursor-pointer hover:bg-green-200 transition items-center justify-center px-3"
              @click="storeVCF"
              title="Save Store Contact"
            >
              <span class="text-xs block text-center mt-1">⬇️ Store</span>
              <img
                src="./assets/priyamfoods_vcf.jpg"
                class="h-full w-full max-h-[30px] object-contain mx-auto"
              />
            </div>
          </div>

          <input
            v-model="email"
            type="email"
            placeholder="Email"
            class="w-full p-4 rounded-xl border-gray-200 border focus:ring-2 focus:ring-orange-500 outline-none"
          />
          <textarea
            v-model="address"
            placeholder="Full Delivery Address & Special requests (like delivery date/time, allergies, etc.)"
            class="w-full p-4 rounded-xl border-gray-200 border focus:ring-2 focus:ring-orange-500 outline-none h-32"
          ></textarea>
          <div class="mt-5 mb-3 text-sm text-gray-600 italic">
            <span class="font-bold text-red-500">* </span>
            <template v-if="contactPlatform === 'whatsapp'">
              <span class="font-bold text-blue-500">Download our contact vCard</span>
              by clicking the Store icon. This will allow you to easily find us
              on WhatsApp and place your order. 
            </template>
            Save our contact in your phone/Telegram for smoother experience (+4915207287460 | Priyam Foods).
            After filling in your details and
            selecting your items, click the "Send Order" button to
            send your order directly to our {{ contactPlatform === 'whatsapp' ? 'WhatsApp' : 'Telegram' }}. We will confirm your order
            and delivery details through {{ contactPlatform === 'whatsapp' ? 'WhatsApp' : 'Telegram' }}. Thank you for choosing Priyam
            Foods!
          </div>
          <button
            @click="submitOrder"
            class="w-full py-5 bg-orange-600 hover:bg-orange-700 text-white text-xl font-bold rounded-2xl shadow-lg transform active:scale-95 transition-all"
          >
            🚀 Send Order via {{ contactPlatform === 'whatsapp' ? 'WhatsApp' : 'Telegram' }}
          </button>
        </div>
      </div>
    </div>

    <footer className="bg-orange-50 text-center py-6 mt-auto">
      <div className="max-w-5xl mx-auto px-6">
        <p className="text-gray-600 text-sm">
          &copy; {{new Date().getFullYear()}} <strong>PRIYAM FOODS</strong> | 
          Developed by <strong>Ravivarma Singaravelu</strong>
        </p>
        
        <div className="text-gray-500 text-xs mt-2 space-y-1">
          <p>
            <strong>Legal Notice:</strong> Residential address withheld for privacy; 
            available upon request for verification. | <strong>Location:</strong> 01589 Riesa, Sachsen, Germany
          </p>
          <p>
            <strong>Contact:</strong> raviamrav@yahoo.com | <strong>Privacy:</strong> GDPR Compliant
          </p>
          <p className="italic pt-2">
            This project is a non-commercial portfolio piece used to demonstrate 
            Full-Stack Engineering skills.
          </p>
          <p>Check out my <a href="https://convocation-gown-system.vercel.app/" class="text-blue-500 hover:underline" target="_blank">Convocation Gown Rental System</a></p>
        </div>
      </div>
    </footer>
    <Analytics />
  </div>
</template>
