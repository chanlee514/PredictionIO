/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import UnidocKeys._
import scala.math.Ordering.Implicits._

lazy val profiles: Map[String, Profile] =
  Map(
    "scala-2.10" -> Profile(
      name="scala-2.10",
      scalaVersion="2.10.5",
      sparkVersion="1.6.2",
      hadoopVersion="2.6.4",
      akkaVersion="2.3.15",
      elasticsearchVersion="1.7.6"),

    "scala-2.11" -> Profile(
      name="scala-2.11",
      scalaVersion="2.11.8",
      sparkVersion="2.0.2",
      hadoopVersion="2.7.3",
      akkaVersion="2.4.10",
      elasticsearchVersion="5.1.2"))

lazy val defaultProfile = "scala-2.10"

buildProfile := {
  val profileName = sys.props.get("build.profile").getOrElse(defaultProfile)
  val profile = profiles(profileName)

  val sparkVersion = sys.props.get("spark.version") map { sv =>
    if ((versionMajor(sv), versionMinor(sv)) < (1, 6)) {
      throw new IllegalArgumentException("Spark versions below 1.6 are no longer supported")
    } else {
      sv
    }
  } getOrElse(profile.sparkVersion)

  val hadoopVersion = sys.props.get("hadoop.version").getOrElse(profile.hadoopVersion)

  if (hadoopVersion != profile.hadoopVersion || sparkVersion != profile.sparkVersion) {
    profile.copy(
      name = profile.name + "-custom",
      sparkVersion = sparkVersion,
      hadoopVersion = hadoopVersion)
  } else {
    profile
  }
}


name := "apache-predictionio-parent"

version in ThisBuild := "0.11.0-SNAPSHOT"

organization in ThisBuild := "org.apache.predictionio"

scalaVersion in ThisBuild := {
  val version = buildProfile.value.scalaVersion
  if (versionMinor(version) < 11) {
    sLog.value.warn(s"Scala version ${version} is deprecated!")
  }
  version
}

scalacOptions in ThisBuild ++= Seq("-deprecation", "-unchecked", "-feature")

scalacOptions in (ThisBuild, Test) ++= Seq("-Yrangepos")
fork in (ThisBuild, run) := true

javacOptions in (ThisBuild, compile) ++= Seq("-source", "1.7", "-target", "1.7",
  "-Xlint:deprecation", "-Xlint:unchecked")

elasticsearchVersion in ThisBuild := buildProfile.value.elasticsearchVersion

akkaVersion in ThisBuild := buildProfile.value.akkaVersion

json4sVersion in ThisBuild := "3.2.10"

sparkVersion in ThisBuild := buildProfile.value.sparkVersion

hadoopVersion in ThisBuild := buildProfile.value.hadoopVersion

val pioBuildInfoSettings = buildInfoSettings ++ Seq(
  sourceGenerators in Compile <+= buildInfo,
  buildInfoKeys := Seq[BuildInfoKey](
    name,
    version,
    scalaVersion,
    sbtVersion,
    sparkVersion,
    hadoopVersion,
    elasticsearchVersion),
  buildInfoPackage := "org.apache.predictionio.core")

// Used temporarily to modify genjavadoc version to "0.10" until unidoc updates it
val genjavadocSettings: Seq[sbt.Def.Setting[_]] = Seq(
  libraryDependencies += compilerPlugin("com.typesafe.genjavadoc" %% "genjavadoc-plugin" % "0.10" cross CrossVersion.full),
    scalacOptions <+= target map (t => "-P:genjavadoc:out=" + (t / "java")))

// Paths specified below are required for the tests, since thread pools initialized
// in unit tests of data subproject are used later in spark jobs executed in core.
// They need to have properly configured classloaders to load core classes for spark
// in subsequent tests.
def coreClasses(baseDirectory: java.io.File, scalaVersion: String) = Seq(
  baseDirectory / s"../core/target/scala-${versionPrefix(scalaVersion)}/classes",
  baseDirectory / s"../core/target/scala-${versionPrefix(scalaVersion)}/test-classes")

val conf = file(".") / "conf"

val commonSettings = Seq(autoAPIMappings := true)

val common = (project in file("common")).
  settings(commonSettings: _*).
  settings(genjavadocSettings: _*).
  settings(unmanagedClasspath in Test += conf)

val data = (project in file("data")).
  dependsOn(common).
  settings(commonSettings: _*).
  settings(genjavadocSettings: _*).
  settings(unmanagedClasspath in Test += conf).
  settings(unmanagedSourceDirectories in Compile +=
    sourceDirectory.value / s"main/spark-${versionMajor(sparkVersion.value)}").
  settings(excludeFilter in unmanagedSources := HiddenFileFilter || {
    val unusedVersion = if (versionMajor(elasticsearchVersion.value) > 1) "" else "5"
    val unusedSource = (sourceDirectory.value / "main" / "scala" / "org" / "apache" / "predictionio" /
      "data" / "storage" / s"elasticsearch${unusedVersion}").getCanonicalPath
    new SimpleFileFilter(_.getCanonicalPath startsWith unusedSource)
  }).
  settings(fullClasspath in Test ++= coreClasses(baseDirectory.value, scalaVersion.value))

val core = (project in file("core")).
  dependsOn(data).
  settings(commonSettings: _*).
  settings(genjavadocSettings: _*).
  settings(pioBuildInfoSettings: _*).
  enablePlugins(SbtTwirl).
  settings(unmanagedClasspath in Test += conf)

val tools = (project in file("tools")).
  dependsOn(core).
  dependsOn(data).
  settings(commonSettings: _*).
  settings(genjavadocSettings: _*).
  enablePlugins(SbtTwirl).
  settings(unmanagedClasspath in Test += conf).
  settings(fullClasspath in Test ++= coreClasses(baseDirectory.value, scalaVersion.value))

val e2 = (project in file("e2")).
  settings(commonSettings: _*).
  settings(genjavadocSettings: _*).
  settings(unmanagedClasspath in Test += conf).
  settings(fullClasspath in Test ++= coreClasses(baseDirectory.value, scalaVersion.value))

val root = (project in file(".")).
  settings(commonSettings: _*).
  // settings(scalaJavaUnidocSettings: _*).
  settings(unidocSettings: _*).
  settings(
    scalacOptions in (ScalaUnidoc, unidoc) ++= Seq(
      "-groups",
      "-skip-packages",
      Seq(
        "akka",
        "org.apache.predictionio.annotation",
        "org.apache.predictionio.authentication",
        "org.apache.predictionio.configuration",
        "org.apache.predictionio.controller.html",
        "org.apache.predictionio.controller.java",
        "org.apache.predictionio.data.api",
        "org.apache.predictionio.data.view",
        "org.apache.predictionio.tools",
        "scalikejdbc").mkString(":"),
      "-doc-title",
      "PredictionIO Scala API",
      "-doc-version",
      version.value,
      "-doc-root-content",
      "docs/scaladoc/rootdoc.txt")).
  settings(
    javacOptions in (JavaUnidoc, unidoc) := Seq(
      "-subpackages",
      "org.apache.predictionio",
      "-exclude",
      Seq(
        "org.apache.predictionio.controller.html",
        "org.apache.predictionio.data.api",
        "org.apache.predictionio.data.view",
        "org.apache.predictionio.data.webhooks.*",
        "org.apache.predictionio.workflow",
        "org.apache.predictionio.tools",
        "org.apache.hadoop").mkString(":"),
      "-windowtitle",
      "PredictionIO Javadoc " + version.value,
      "-group",
      "Java Controllers",
      Seq(
        "org.apache.predictionio.controller.java",
        "org.apache.predictionio.data.store.java").mkString(":"),
      "-group",
      "Scala Base Classes",
      Seq(
        "org.apache.predictionio.controller",
        "org.apache.predictionio.core",
        "org.apache.predictionio.data.storage",
        "org.apache.predictionio.data.storage.elasticsearch.*",
        "org.apache.predictionio.data.storage.elasticsearch5.*",
        "org.apache.predictionio.data.store").mkString(":"),
      "-overview",
      "docs/javadoc/javadoc-overview.html",
      "-noqualifier",
      "java.lang")).
  aggregate(
    common,
    core,
    data,
    tools,
    e2)

val pioUnidoc = taskKey[Unit]("Builds PredictionIO ScalaDoc")

pioUnidoc := {
  (unidoc in Compile).value
  val log = streams.value.log
  log.info("Adding custom styling.")
  IO.append(
    crossTarget.value / "unidoc" / "lib" / "template.css",
    IO.read(baseDirectory.value / "docs" / "scaladoc" / "api-docs.css"))
  IO.append(
    crossTarget.value / "unidoc" / "lib" / "template.js",
    IO.read(baseDirectory.value / "docs" / "scaladoc" / "api-docs.js"))
}

homepage := Some(url("http://predictionio.incubator.apache.org"))

pomExtra := {
  <parent>
    <groupId>org.apache</groupId>
    <artifactId>apache</artifactId>
    <version>18</version>
  </parent>
  <scm>
    <connection>scm:git:github.com/apache/incubator-predictionio</connection>
    <developerConnection>scm:git:https://git-wip-us.apache.org/repos/asf/incubator-predictionio.git</developerConnection>
    <url>github.com/apache/incubator-predictionio</url>
  </scm>
  <developers>
    <developer>
      <id>donald</id>
      <name>Donald Szeto</name>
      <url>http://predictionio.incubator.apache.org</url>
      <email>donald@apache.org</email>
    </developer>
  </developers>
}

childrenPomExtra in ThisBuild := {
  <parent>
    <groupId>{organization.value}</groupId>
    <artifactId>{name.value}_{scalaBinaryVersion.value}</artifactId>
    <version>{version.value}</version>
  </parent>
}

concurrentRestrictions in Global := Seq(
  Tags.limit(Tags.CPU, 1),
  Tags.limit(Tags.Network, 1),
  Tags.limit(Tags.Test, 1),
  Tags.limitAll( 1 )
)

parallelExecution := false

parallelExecution in Global := false

testOptions in Test += Tests.Argument("-oDF")

printProfile := {
  val profile = buildProfile.value
  println(s"PROFILE_NAME=${profile.name}")
  println(s"SCALA_VERSION=${profile.scalaVersion}")
  println(s"SPARK_VERSION=${profile.sparkVersion}")
  println(s"HADOOP_VERSION=${profile.hadoopVersion}")
  println(s"AKKA_VERSION=${profile.akkaVersion}")
  println(s"ELASTICSEARCH_VERSION=${profile.elasticsearchVersion}")
}
