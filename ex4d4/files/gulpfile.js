//
// Variables ===================================
//

// Load dependencies
const autoprefixer = require('gulp-autoprefixer');
const cleancss = require('gulp-clean-css');
const gulp = require('gulp');
const npmdist = require('gulp-npm-dist');
const sass = require('gulp-sass');
const uglify = require('gulp-uglify');
const concat = require('gulp-concat');

// Define paths
const paths = {
  base:   {
    base:         {
      dir:    './'
    },
    node:         {
      dir:    './node_modules'
    },
    packageLock:  {
      files:  './package-lock.json'
    }
  },
  src: {
    base : {
      dir: './src',
      fiels: '.src/**/*'
    },
    js: {
      dir:    './src/js',
      files:  './src/js/**/*',
    },
    scss: {
      dir:    './src/scss',
      files:  './src/scss/**/*',
      main:   './src/scss/*.scss'
    }
  },
  dist:   {
    base:   {
      dir:    './dist',
      files:  './dist/**/*'
    },
    libs:   {
      dir:    './dist/libs'
    },
    js: {
      dir:    './dist/js',
      files:  './dist/js/**/*',
    },
    css:    {
      dir:    './dist/css',
      files:  './dist/css/**/*'
    },
    img:    {
      dir:    './dist/img',
      files:  './dist/img/**/*',
    },
  }
};


//
// Tasks ===================================
//

gulp.task('watch', function() {
  gulp.watch(paths.src.scss.files, gulp.series('scss'));
});

gulp.task('scss', function() {
  return gulp
  .src(paths.src.scss.main)
  .pipe(sass().on('error', sass.logError))
  .pipe(autoprefixer())
  .pipe(cleancss())
  .pipe(gulp.dest(paths.dist.css.dir));
});

gulp.task('js', function() {
  return gulp
  .src([
    paths.src.js.files
    ])
  .pipe(concat('theme.min.js'))
  .pipe(uglify())
  .pipe(gulp.dest(paths.dist.js.dir));
});

gulp.task('copy:libs', function() {
  return gulp
  .src(npmdist(), { base: paths.base.node.dir })
  .pipe(gulp.dest(paths.dist.libs.dir));
});

gulp.task('build', gulp.series('copy:libs'));

gulp.task('default', gulp.series('scss', 'watch'));

gulp.task('setup', gulp.parallel('copy:libs', 'scss', 'js'))
