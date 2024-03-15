<template>
  <div>
    <h1 class="heading">欢迎使用阻燃小助手!</h1>
    <p class="text">请在下方输入配方数据:</p>
    <p class="footnote">输入时请统一计量单位，模型会按照原料百分比进行计算</p>
    <div class="container">
      <label for="matrix">基底（聚丙烯PP）用量：</label>
      <input id="matrix" type="text" v-model="matrixWeight" @input="matrixValid" required>
    </div>
    <div class="container">
      <label for="antioxygen">抗氧剂（AO）用量：</label>
      <input id="antioxygen" type="text" v-model="antioxygenWeight" @input="antioxygenValid" required>
    </div>
    <div class="container" v-for="(filler, index) in fillers" :key="index">
      <label>
        原料种类:
        <select v-model="filler.type">
          <option value="" disabled selected>请选择原料种类</option>
          <option v-for="fillerType in fillerTypes" :key="fillerType">{{ fillerType }}</option>
        </select>
      </label>
      <label>
        原料用量:<input type="text" v-model="filler.weight" @input="fillersValid" required>
      </label>
      <button @click="deleteFiller(index);fillersValid()">删除原料</button>
    </div>
    <button @click="addFiller();fillersValid()">添加原料</button>
    <button @click="validateForm();performPrediction()">预测</button>
    <p v-if="showRequiredFieldError" style="color: red;">请以正确的形式填写必填项</p>
    <div v-if="isLoading && !predictionResult">
      <p>模型预测中...</p>
    </div>
    <div v-if="predictionResult">
    <!-- 如果 predictionResult 数据属性有值，那么这个 <div> 将会被渲染出来并显示相关内容。 -->
      <h2>阻燃性能（LOI值）：{{ predictionResult }}</h2>
      <div class="feedback">
        <p>若预测值与您的实际测量值误差较大，可能有以下一些原因：</p>
        <div class="reason">
          <p>1.实验环境温度</p>
          <p>2.工艺</p>
          <p>3.时间</p>
        </div>
        <p>请优化实验条件后再次实验。</p>
      </div> 
      <div class="feedback">
        <p>如果问题仍然存在，请提供更多详细信息，或者联系我们，以便我们为您提供更准确的帮助</p>
        <p>我们的联系方式是：1364332376@shu.edu.cn</p>
      </div>
      <div class="container">
        <label for="real_loi">您的氧指数测量值：</label>
        <input id="real_loi" type="text" v-model="real_loi" />
      </div>
      <div class="container-env">
        <label for="real_env">简述您的实验环境：</label>
        <input id="real_env" type="text" v-model="real_env" class="env_input"/> 
        <div class="submit">
          <button @click="feedbacksaving" style="display: inline; margin-right: 20px;">提交数据</button>
          <p v-if="showThankYouMessage" style="display: inline;">信息已提交，感谢您的反馈!</p>
        </div> 
      </div>
    </div>
  </div>
</template>
  
  <script>
  import axios from 'axios';
  export default {
    data() {
      return {
        //基底重量
        matrixWeight: '',
        //抗氧剂重量
        antioxygenWeight: '',
        //原料配方数组,数组初始大小为3条配方数据
        fillers: [
          { type: '', weight: '' },
          { type: '', weight: '' },
          { type: '', weight: '' }
        ],
        //原料种类
        fillerTypes:[
        '十溴二苯乙烷（DBDPE）','羟基锡酸锌（ZHS）','锡酸锌（ZS）','三氧化二锑（Sb2O3）','氢氧化镁（Mg(OH)2）',
        'BDBNCE（溴系阻燃剂）','六溴环十二烷','四溴二苯甲基二醇','十溴二苯醚','滑石粉','得克隆','硼酸锌','双（四溴邻苯二甲酰亚胺）乙烷',
        '双（五溴苯基）乙烷','2,2-双-（溴甲基）-3-溴-1-丙醇磷酸酯','丙烯酸五溴苄基酯（PBBA）和三元乙丙橡胶（EPDM）共聚获得的母料',
        '其他添加剂','聚丙烯酸五溴苄基酯','三元乙丙橡胶','2-乙基己基二苯基磷酸酯','聚磷酸铵','聚磷酸铵-混合膨胀型阻燃剂',
        '聚磷酸铵和季戊四醇混合物','聚磷酸铵和异氰脲酸酯三羟乙基酯混合物','膨胀阻燃剂','聚磷酸铵、季戊四醇和苯甲酸酯混合物',
        '聚磷酸铵-混合膨胀型阻燃剂','氢氧化铝','混合膨胀型阻燃剂','氢氧化镁（MAGNIFIN H10）','氢氧化镁（MAGNIFIN H10F）','包覆红磷',
        '硅阻燃剂','硬脂酸镁','膨胀石墨','磷系阻燃剂','三聚氰胺磷酸盐','双季戊四醇','三聚氰胺','三聚氰胺氰尿酸盐','磷酸二甲胺',
        '硼酸三聚氰胺','酚醛树脂1','聚2,6-二甲基亚苯基醚','酚醛树脂2','季戊四醇','三嗪基大分子','炭化发泡剂','季戊四醇磷酸酯',
        '含磷纳米阻燃剂','一种新型聚硅氧烷','基于多金属氧酸盐的离子液体（PIL）杂化材料[BMIm]3PW (PIL1)',
        '基于多金属氧酸盐的离子液体（PIL）杂化材料[BMIm]3PMo (PIL2)','基于多金属氧酸盐的离子液体（PIL）杂化材料[BMIm]4SiW (PIL3)',
        '多金属氧酸盐基有机-无机杂化材料','聚金属氧基离子液体有机部分烷基[C4]PMo(PIL4)','聚金属氧基离子液体有机部分烷基[C8]PMo(PIL8)',
        '聚金属氧基离子液体有机部分烷基[C12]PMo(PIL12)','聚金属氧基离子液体有机部分烷基[C18]PMo(PIL18)','二氧化硅',
        '金属氧化物2','金属氧化物1','镍','镍-铝','镍-镁','镍-铜','醋酸镍','氯化镍','硫酸镍','碳酸镍','氧化镍','聚二甲基硅氧烷',
        'N-烷氧基受阻胺（Flamestab NOR116）','螺双磷酰双氰胺','二氧化镍','氧化锰','氧化钛','氧化锌','氧化锰','溴化环氧树脂','蒙托土','玻璃泡',
        'α-磷酸锆','氧化镧','9,10-二氢-9-氧杂-10-磷杂菲-10-氧化物（DOPO）','1-氧代-4-羟基-甲基-2,6,7-三氧代-1-磷杂双环[2.2.2]辛烷'
        ],
        //判断必填项是否全部正确填写
        isMatrixValid: false,
        isAntioxygenValid: false,
        isFillersValid: false,
        isFormValid: false,
        //提示输入错误
        showRequiredFieldError: false,
        //预测结果
        predictionResult: '',
        //predictionResult: { LOI: '', UL_94: '', 拉伸强度: '', 弯曲强度: '', 缺口冲击强度: '', 无缺口冲击强度: ''}
        //加载状态
        isLoading: false, 
        //感谢反馈信息状态
        showThankYouMessage:false,
        //测试
        test:false,
        test2:false,
      }
    },
    methods: {
      addFiller() {
      // 添加一个新的空白原料条目到 materials 数组
        this.fillers.push({ type: '', weight: '' });
      },
      deleteFiller(index) {
      // 删除一个原料条目
        this.fillers.splice(index, 1);
      },
      matrixValid() {
      // 判断基底输入数据是否合法
        this.isMatrixValid = /^\d+$/.test(this.matrixWeight);
      },
      antioxygenValid() {
      // 判断基底输入数据是否合法
        this.isAntioxygenValid = /^\d+$/.test(this.antioxygenWeight);
      },
      fillersValid() {
      // 判断填料输入数据是否合法
        this.isFillersValid = this.fillers.every(filler => {
          return filler.type !== "" && /^\d+$/.test(filler.weight);
        })
      },
      validateForm() {
      // 判断表单是否有效
        this.isFormValid = this.isMatrixValid && this.isAntioxygenValid && this.isFillersValid;
        this.showRequiredFieldError = !this.isFormValid;
      },
      performPrediction() {
        if (this.isFormValid){
          this.predictionResult = '';
          this.isLoading = true; //开始加载
          const fillersData = JSON.stringify(this.fillers);
          axios.get('http://localhost:5000/predict', {
            params: {
              matrix: this.matrixWeight,
              antioxygen: this.antioxygenWeight,
              fillers: fillersData
            }
          })
          .then(response => {
            this.predictionResult = response.data.result; 
          })
          .catch(error => {
            console.error(error);
          })
          .finally(() => {
            this.isLoading = false; // 停止加载
          });
        }
      },
      feedbacksaving() {
      // 保存用户提供的数据
        const fillersData = JSON.stringify(this.fillers);
        axios.get('http://localhost:5000/feedback', {
          params: {
            matrix: this.matrixWeight,
            antioxygen: this.antioxygenWeight,
            fillers: fillersData,
            predictionResult: this.predictionResult,
            real_loi: this.real_loi,
            real_env: this.real_env
          }
       })
        .then(response => {
          const completedMessage = response.data.message;
          this.showThankYouMessage = true;
          console.log(completedMessage); // 打印成功消息
       })
        .catch(error => {
          console.error(error);
        });
      }
    }
  };
  </script>
  
  <style scoped>
  /* 可以在这里添加组件特定的样式 */
  .heading { /* 欢迎使用阻燃小助手! */
  text-align: left; /* 将内容左对齐 */
  margin-left: 100px; /* 设置左边距为 100px */
  }
  .text { /* 请在下方输入配方数据 */
  text-align: left; /* 将内容左对齐 */
  margin-left: 100px; /* 设置左边距为 100px */
  font-weight: bold;
  }
  .footnote { /* 输入时请统一计量单位 */
  text-align: left; /* 将内容左对齐 */
  margin-left: 120px; /* 设置左边距为 100px */
  font-style: italic; /*设置斜体 */
  }
  .container {
  text-align: left; /* 将内容左对齐 */
  margin-left: 150px; /* 设置左边距为 100px */
  }
  .feedback {
  text-align: left; /* 将内容左对齐 */
  margin-left: 150px; /* 设置左边距为 150px */
  font-style: italic; /*设置斜体 */
  margin-top: 40px; /* 设置上边距为 20 像素 */
  }
  .reason {
  font-size: 14px; /* 设置字体大小 */
  text-align: left; /* 将内容左对齐 */
  margin-left: 20px; /* 设置左边距为 150px */
  }
  .container-env {
  text-align: left; /* 将内容左对齐 */
  margin-left: 150px; /* 设置左边距 */
  margin-top: 15px; /* 设置上边距 */
  }
  .env_input {
  width: 200px; /* 设置宽度 */
  height: 80px; /* 设置高度 */
  }
  .submit {
  margin-left: 260px; /* 设置左边距 */
  margin-top: 10px; /* 设置上边距 */
  }
  </style>
