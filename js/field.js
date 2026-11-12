(function () {
  var canvas = document.querySelector("[data-field]");
  if (!canvas || !document.documentElement.classList.contains("motion")) return;
  if (!window.matchMedia("(min-width: 900px)").matches) return;
  var gl = canvas.getContext("webgl", { alpha: true, antialias: false, premultipliedAlpha: true, powerPreference: "low-power" });
  if (!gl) return;

  function compile(type, src) {
    var shader = gl.createShader(type);
    gl.shaderSource(shader, src);
    gl.compileShader(shader);
    return shader;
  }

  var program = gl.createProgram();
  gl.attachShader(program, compile(gl.VERTEX_SHADER, "attribute vec2 a;void main(){gl_Position=vec4(a,0.0,1.0);}"));
  gl.attachShader(program, compile(gl.FRAGMENT_SHADER, [
    "precision mediump float;",
    "uniform vec2 uRes;",
    "uniform float uTime;",
    "uniform vec2 uMouse;",
    "uniform vec3 uColor;",
    "void main(){",
    "  vec2 uv=gl_FragCoord.xy/uRes;",
    "  vec2 p=uv-0.5;",
    "  p.x*=uRes.x/uRes.y;",
    "  vec2 m=(uMouse-0.5)*vec2(uRes.x/uRes.y,1.0);",
    "  float wave=sin(p.x*2.4+uTime*0.16+m.x*0.8)*0.08;",
    "  wave+=sin(p.x*5.0-uTime*0.11+m.y)*0.035;",
    "  float band=smoothstep(0.09,0.0,abs(p.y*0.85-wave));",
    "  float band2=smoothstep(0.06,0.0,abs(p.y*1.15-wave*0.6+0.16));",
    "  float v=band*0.55+band2*0.28;",
    "  v*=smoothstep(1.15,0.15,length(p));",
    "  gl_FragColor=vec4(uColor*v,v);",
    "}"
  ].join("\n")));
  gl.linkProgram(program);
  gl.useProgram(program);

  var buf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
  var loc = gl.getAttribLocation(program, "a");
  gl.enableVertexAttribArray(loc);
  gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
  gl.enable(gl.BLEND);
  gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);

  var uRes = gl.getUniformLocation(program, "uRes");
  var uTime = gl.getUniformLocation(program, "uTime");
  var uMouse = gl.getUniformLocation(program, "uMouse");
  var uColor = gl.getUniformLocation(program, "uColor");
  var mouse = [0.72, 0.38];
  var target = [0.72, 0.38];
  var start = performance.now();
  var running = true;
  var visible = true;

  function accent() {
    var probe = document.createElement("span");
    probe.style.color = "var(--accent)";
    document.body.appendChild(probe);
    var c = getComputedStyle(probe).color;
    probe.remove();
    var m = c.match(/[\d.]+/g) || [12, 68, 124];
    return [m[0] / 255, m[1] / 255, m[2] / 255];
  }
  var color = accent();

  function resize() {
    var rect = canvas.getBoundingClientRect();
    var dpr = Math.min(window.devicePixelRatio || 1, 1.25);
    var w = Math.max(1, Math.floor(rect.width * dpr));
    var h = Math.max(1, Math.floor(rect.height * dpr));
    if (canvas.width !== w || canvas.height !== h) {
      canvas.width = w;
      canvas.height = h;
    }
    gl.viewport(0, 0, canvas.width, canvas.height);
  }
  resize();
  window.addEventListener("resize", resize);

  window.addEventListener("pointermove", function (event) {
    var rect = canvas.getBoundingClientRect();
    if (!rect.width) return;
    target[0] = (event.clientX - rect.left) / rect.width;
    target[1] = 1 - (event.clientY - rect.top) / rect.height;
  });

  var observer = new IntersectionObserver(function (entries) {
    visible = entries[0].isIntersecting;
  }, { threshold: 0.05 });
  observer.observe(canvas);
  document.addEventListener("visibilitychange", function () {
    running = !document.hidden;
  });

  var themeBtn = document.querySelector("[data-theme-toggle]");
  if (themeBtn) themeBtn.addEventListener("click", function () { color = accent(); });

  function frame(now) {
    requestAnimationFrame(frame);
    if (!running || !visible) return;
    mouse[0] += (target[0] - mouse[0]) * 0.04;
    mouse[1] += (target[1] - mouse[1]) * 0.04;
    gl.uniform2f(uRes, canvas.width, canvas.height);
    gl.uniform1f(uTime, (now - start) / 1000);
    gl.uniform2f(uMouse, mouse[0], mouse[1]);
    gl.uniform3f(uColor, color[0], color[1], color[2]);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  }
  requestAnimationFrame(frame);
})();
