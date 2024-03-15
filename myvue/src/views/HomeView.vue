<template>
  <div class="home">
    <img alt="framework" src="/images/framework.png" style="width: 600px; height: 300px; margin-top: 20px;">
    <!-- alt: 用于指定图片的替代文本，即在图片无法加载时显示的文本 -->
    <!-- src: 用于指定图片的来源地址，即图片的 URL 或文件路径 -->
    <HelloWorld msg="Welcome to Your Flame retardant assistant"/>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'//导入组件HelloWorld
export default {
  name: 'HomeView',
  components: {  //将HelloWorld 组件注册为子组件
    HelloWorld   //是"HelloWorld:HelloWorld"的简写
  }
}
</script>
