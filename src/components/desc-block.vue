<template>
  <div class="desc-block">
    <div class="description">
      <slot name="desc"></slot>
    </div>
    <div class="wx">
      <slot name="wx"></slot>
    </div>
  </div>
</template>

<style>
  .desc-block {
    border: solid 1px #eaeefb;
    border-radius: 4px;
    transition: .2s;
    background-color: rgb(249, 250, 252);
    clear: both;
    overflow: hidden;
    margin-bottom: 10px;
  }
  .wx {
    width: 60%;
    border-right: 1px solid rgb(234, 238, 251);
    margin-bottom: 20px;
  }

  .description {
    padding: 18px 24px;
    width: 40%;
    box-sizing: border-box;
    border-left: solid 1px #eaeefb;
    float: right;
    font-size: 14px;
    line-height: 1.8;
    color: #5e6d82;
    word-break: break-word;
  }
  code {
    color: rgb(94, 109, 130);
    background-color: rgb(230, 239, 251);
    display: inline-block;
    font-size: 12px;
    height: 18px;
    line-height: 18px;
    margin: 0px 4px;
    padding: 1px 5px;
    border-radius: 3px;
  }
</style>